from airflow.decorators import task
import pandas as pd
import os

PROJECT_ID = os.getenv('PROJECT_ID', 'fasttrack-poc')
MAPPING_FILE = os.getenv('MAPPING_FILE', 'column_mapping - mapping.csv')

@task(task_id="get_column_mapping")
def get_column_mapping():
    df = pd.read_csv(
        f'gs://supplier-column-mapping-{PROJECT_ID}/{MAPPING_FILE}',
        low_memory = False,
        dtype = str
    )
    return df.to_json()