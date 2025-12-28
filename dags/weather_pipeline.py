from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Import the logic from your modules
from weather_modules.database import WeatherDatabase
from weather_modules.extractor import fetch_raw_weather
from weather_modules.transformer import transform_weather_data, create_upsert_op
from weather_modules.config import CITIES

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def setup_db():
    """Task to ensure Mongo indexes exist."""
    db = WeatherDatabase()
    db.ensure_indexes()
    print("Database indexes ensured.")

def run_weather_etl():
    """Main ETL Task."""
    db = WeatherDatabase()
    ops = []
    
    for c in CITIES:
        try:
            # Extract
            raw = fetch_raw_weather(c['name'], c['country'])
            # Transform
            clean = transform_weather_data(raw, c['name'], c['country'])
            # Create MongoDB Op
            ops.append(create_upsert_op(clean))
        except Exception as e:
            print(f"Failed to process {c['name']}: {e}")

    # Load
    if ops:
        db.bulk_upsert(ops)
    else:
        print("No operations to perform.")

# Define the DAG
with DAG(
    'weather_ingestion_pipeline',
    default_args=default_args,
    description='Fetch weather data, transform, and load to MongoDB',
    schedule_interval='@hourly',  # Runs every hour
    catchup=False
) as dag:

    t1 = PythonOperator(
        task_id='ensure_database_indexes',
        python_callable=setup_db,
    )

    t2 = PythonOperator(
        task_id='fetch_and_load_weather',
        python_callable=run_weather_etl,
    )

    # Set dependencies
    t1 >> t2