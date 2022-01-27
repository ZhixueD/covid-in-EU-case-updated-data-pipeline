"""Example Airflow DAG that install packages and download data from website into GCS, run dataflow to do data cleaning and load the final 
two tables to Bigquery for later analyze.
This DAG relies on three Airflow variables

* project_id - Google Cloud Project ID to use for the Cloud Dataflow cluster.
* gce_zone - Google Compute Engine zone where Cloud Dataflow cluster should be
  created.
* gce_region - Google Compute Engine region where Cloud Dataflow cluster should be
  created.
"""
import datetime
import os
from airflow import models
from airflow.operators.bash_operator import BashOperator
from airflow.providers.apache.beam.operators.beam import BeamRunPythonPipelineOperator
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.dataflow import DataflowConfiguration

bucket_path = models.Variable.get("bucket_path")
project_id = models.Variable.get("project_id")
gce_region = models.Variable.get("gce_region")


default_args = {
    # Tell airflow to start one day ago, so that it runs as soon as you upload it
    "start_date": days_ago(1),
    "dataflow_default_options": {
        "project": project_id,
        # Set to your region
        "region": gce_region,
        # Set to your zone
    },
}

# Define a DAG (directed acyclic graph) of tasks.
# Any task you create within the context manager is automatically added to the
# DAG object.


with models.DAG(
    # The id you will see in the DAG airflow page
    "covid_composer_dataflow_dag",
    default_args=default_args,
    # The interval with which to schedule the DAG
    schedule_interval=datetime.timedelta(days=1),  # Override to match your needs
    ) as dag:

	# define the first task

    first_data_download = BashOperator(
		task_id='first_data_download',
		bash_command='curl https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv | gsutil cp - gs://t-osprey-337221-covid/covid-eu/country.csv',
		dag=dag,
	)
    
    second_data_download = BashOperator(
		task_id='second_data_download',
		bash_command='curl https://opendata.ecdc.europa.eu/covid19/subnationalcasedaily/csv/data.csv | gsutil cp - gs://t-osprey-337221-covid/covid-eu/region.csv',
		dag=dag,
	)
    	
    
    start_python_pipeline_dataflow_runner = BeamRunPythonPipelineOperator(
    task_id="start_python_pipeline_dataflow_runner",
    runner="DataflowRunner",
    py_file='gs://t-osprey-337221-covid/dataflow_etl_bigquery.py',
    pipeline_options={
        'tempLocation': 'gs://{0}/staging/'.format(bucket_path),
        'stagingLocation': 'gs://{0}/staging/'.format(bucket_path),
    },
    py_options=[],
    py_requirements=['apache-beam[gcp]==2.35.0','apache_beam[dataframe]'],
    py_interpreter='python3',
    py_system_site_packages=False,
    dataflow_config=DataflowConfiguration(
        job_name='{{task.task_id}}', project_id='{0}'.format(project_id), location="europe-north1"
    ),
    )
    
first_data_download >> second_data_download >> start_python_pipeline_dataflow_runner 