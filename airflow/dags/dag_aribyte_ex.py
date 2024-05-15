from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.operators.bash import BashOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor
from airflow.sensors.filesystem import FileSensor
import pendulum


from airflow.decorators import dag, task
from airflow.providers.dbt.cloud.hooks.dbt import DbtCloudHook, DbtCloudJobRunStatus
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from pendulum import datetime

DBT_CLOUD_CONN_ID = "dbtconn"
JOB_ID = "70403103921340"

with DAG(dag_id='trigger_airbyte_job_example',
         default_args={'owner': 'airflow'},
         schedule_interval='@daily',
         start_date=days_ago(1)
    ) as dag:

    
    trigger_airbyte_sync = AirbyteTriggerSyncOperator(
        task_id='airbyte_trigger_file_feather_sync', #Nombre que le he dado al trigger
        airbyte_conn_id='airflow_call_airbyte',#Conexion creada desde el UI de conexiones de Airflow
        connection_id='10aab3f3-a3fe-4fff-b776-007900a0ff31', #Id asignado por Airbyte al conector creado desde el UI de Airbyte
        asynchronous=True
    )

    trigger_airbyte_sync2 = AirbyteTriggerSyncOperator(
        task_id='airbyte_trigger_google_sheets_sync',
        airbyte_conn_id='airflow_call_airbyte',
        connection_id='acfa3d6e-185d-4cdf-85d4-1a9a02de5718',
        asynchronous=True
    )

    trigger_airbyte_sync3 = AirbyteTriggerSyncOperator(
        task_id='airbyte_trigger_pokeapi_sync',
        airbyte_conn_id='airflow_call_airbyte',
        connection_id='7a8d5510-7fd3-4757-9363-79ed5e1ac82b',
        asynchronous=True
    )

    trigger_airbyte_sync4 = AirbyteTriggerSyncOperator(
        task_id='airbyte_trigger_postgres_sync',
        airbyte_conn_id='airflow_call_airbyte',
        connection_id='f9fdb2f6-185d-438d-9abb-9505de5f8681',
        asynchronous=True
    )

    wait_for_sync_completion = AirbyteJobSensor(
        task_id='airbyte_check_sync',
        airbyte_conn_id='airflow_call_airbyte',
        airbyte_job_id=trigger_airbyte_sync.output
    )

    trigger_job = DbtCloudRunJobOperator(
        task_id="trigger_dbt_cloud_job",
        dbt_cloud_conn_id=DBT_CLOUD_CONN_ID,
        job_id=JOB_ID,
        check_interval=600,
        timeout=3600,
    )
    
    [trigger_airbyte_sync,trigger_airbyte_sync2,trigger_airbyte_sync3,trigger_airbyte_sync4] >> wait_for_sync_completion >> trigger_job