from datetime import datetime
import os
import logging
from airflow.decorators import dag
from tasks import (
    column_mapping,
    fast_track
)

CRON_SCHEDULER = os.environ.get("CRON_SCHEDULER")
logging.getLogger().setLevel(logging.INFO)


@dag(
    dag_id='fast-track',
    schedule_interval=None,
    start_date=datetime(2022, 1, 1),
    catchup=False,
    
)
def fast_track_pipeline():
    mapping = column_mapping.get_column_mapping()
    fast_track.load_supplier_files(mapping)


dag = fast_track_pipeline()


if __name__ == "__main__":
    from airflow.utils.state import State
    dag.clear(dag_run_state=State.NONE)
    dag.run()