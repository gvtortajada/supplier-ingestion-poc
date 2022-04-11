from datetime import datetime
import os
import logging
from airflow.decorators import dag
from tasks import pim_to_bq

CRON_SCHEDULER = os.environ.get("CRON_SCHEDULER")
logging.getLogger().setLevel(logging.INFO)


@dag(
    dag_id='pim-to-bq',
    schedule_interval=None,
    start_date=datetime(2022, 1, 1),
    catchup=False,
)
def import_pim_extract_to_bq():
    pim_to_bq.import_pim_extract_to_bq()

dag = import_pim_extract_to_bq()


if __name__ == "__main__":
    from airflow.utils.state import State
    dag.clear(dag_run_state=State.NONE)
    dag.run()