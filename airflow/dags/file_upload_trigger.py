from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from kafka import KafkaConsumer
import subprocess, json

def consume_kafka():
    consumer = KafkaConsumer(
        'file_uploads',
        bootstrap_servers=['kafka:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest'
    )
    for msg in consumer:
        filename = msg.value['filename']
        print(f"New file: {filename}")
        subprocess.run(["python", "/opt/airflow/app/pipeline.py"])

with DAG(
    dag_id='file_upload_trigger',
    start_date=datetime(2025, 8, 26),
    schedule_interval=None,
    catchup=False
) as dag:
    task = PythonOperator(
        task_id='consume_kafka_and_run_pipeline',
        python_callable=consume_kafka
    )
