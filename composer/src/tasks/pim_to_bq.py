from airflow.decorators import task
import pandas as pd
from datetime import datetime
from google.cloud import (
    bigquery, 
    storage
)
import os
from tasks.schemas import get_pim_schema
from tasks.utils import gcs_move_file

bq_client = bigquery.Client()
table_id = 'fasttract.pim-extract'
gcs_client = storage.Client()
PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'fasttrack-poc')

@task(task_id="import_pim_extract_to_bq")
def import_pim_extract_to_bq():
    for blob in gcs_client.list_blobs('pim-import-{PROJECT_ID}'):
        df = pd.read_csv(
            f'gs://pim-import-{PROJECT_ID}/{blob.name}', 
            encoding = "ISO-8859-1", 
            low_memory = False,
            dtype = str
        )
        df['fileName'] = blob.name
        df['importDate'] = datetime.now()
        job_config = bigquery.LoadJobConfig(
            schema = get_pim_schema(),
            write_disposition="WRITE_TRUNCATE",
        ) 
        job = bq_client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()
        gcs_move_file(
            f'pim-import-{PROJECT_ID}',
            blob.name,
            f'pim-import-completed-{PROJECT_ID}',
            blob.name,
            gcs_client
        )
