import datetime
import pendulum
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

with DAG(
    dag_id='pipeline-dag',
    schedule_interval="@daily",
    start_date=pendulum.datetime(2022, 8, 3, tz="UTC"),
) as dag:

        step1_csv = BashOperator(
        task_id="step1_extract_from_csv",
        bash_command="""
   cd $AIRFLOW_HOME/dags/tasks/
   python3 step1_extract_from_csv.py {{ ds }}
   """,
    )

        step1_pg = BashOperator(
        task_id="step1_extract_from_pg",
        bash_command="""
   cd $AIRFLOW_HOME/dags/tasks/
   python3 step1_extract_from_pg.py {{ ds }}
   """,
    )

        step2_load = BashOperator(
        task_id="step2_load_to_finaldb",
        bash_command="""
   cd $AIRFLOW_HOME/dags/tasks/
   python3 step2_load_to_finaldb.py {{ ds }}
   """,
    )
        step3_query = BashOperator(
        task_id="step3_query_orders",
        bash_command="""
   cd $AIRFLOW_HOME/dags/tasks/
   python3 step3_query_orders.py {{ ds }}
   """,
    )

[step1_csv, step1_pg] >> step2_load >> step3_query