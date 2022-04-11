from datetime import datetime
import os
import logging
from airflow.decorators import dag
from tasks import glossary

CRON_SCHEDULER = os.environ.get("CRON_SCHEDULER")
logging.getLogger().setLevel(logging.INFO)


@dag(
    dag_id='translate-glossary',
    schedule_interval=None,
    start_date=datetime(2022, 1, 1),
    catchup=False,
)
def translate_glossary():
    glossary.upsert()

dag = translate_glossary()


if __name__ == "__main__":
    from airflow.utils.state import State
    dag.clear(dag_run_state=State.NONE)
    dag.run()