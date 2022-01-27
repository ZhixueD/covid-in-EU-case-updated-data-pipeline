# Covid-cases-in-EU-dailly-updated-pipeline

![process](https://user-images.githubusercontent.com/98153604/151380489-f4fe3d0c-ca49-4da3-8df6-dff6ad94c9da.png)

## About the dataset
At the request of Member States, data on the daily number of new reported COVID-19 cases and deaths by EU/EEA country will be available to download from 11 March 2021 on European Centre for Disease Prevention and Control website (https://www.ecdc.europa.eu/en/covid-19/data). 

## About this project

In this project, I create an ETL batch data pipeline on google cloud platform by using Dataflow and Composer(AirFlow). The whole workflow covers two daily data download, data upload to Google cloud storage, data transform and cleaning by Dataflow and load data to bigquery. When data in Bigquery, we can analyze data using SQL in Bigquery and connect Tableau to Bigquery for data visulization and analysis.

The project contains follow steps:

1. Enable API used in this project.
2. Create a Composer environment. 
3. Create a Cloud Storage bucket, named: t-osprey-337221-covid
4. Create a bigquery dataset
5. Setting Airflow variables in Airflow web UI
6. Copy the DAG python file to Cloud Storage Dag folder
7. Exploring DAG runs
8. Check the Bigquery
9. Connect to Tableau

## 1. Enable API used in this project

(1) Enable Kubernetes Engine API 

![Kuberne API](https://user-images.githubusercontent.com/98153604/151383877-9e9cfc88-220c-4435-bf44-0e571f1290f4.JPG)

(2) Enable DataFlow API in this project

![dataflow API](https://user-images.githubusercontent.com/98153604/151384087-9136dd81-83fc-442e-b12c-a3137c8965ed.JPG)

(3) Enable Cloud Composer API

![composer API](https://user-images.githubusercontent.com/98153604/151384240-f0e80581-ce74-40b4-a7d8-2339e08fa4b5.JPG)

## 2. Create a Composer environment.
Click CREATE ENVIRONMENT and select Composer 1. Set the following for your environment:
    Name	highcpu
    Location	europe-central2
    Zone	europe-central2-a
    Machine type	n1-highcpu-4
    
 leave others as default
 
 After create
 
 ![airflow10](https://user-images.githubusercontent.com/98153604/151387252-1ac0672f-d8b0-4a9d-ba74-0817b7a51171.JPG)
 
 Go to Computer Engine, it shows:
 
 ![airflow9](https://user-images.githubusercontent.com/98153604/151387485-02ca1712-9dff-4b40-b1ed-67d7eec1fc1a.JPG)
 
 Go to Google cloud storage, you will see a new bucket create:
 
 ![airflow7](https://user-images.githubusercontent.com/98153604/151390976-13b9b3e4-3cd0-4647-bbb5-83e319241de0.JPG)

 ## 3. Create a Cloud Storage bucket, named: t-osprey-337221-covid
 
 The bucket location set to europe-north1 (Finland), Meanwhile create two foders in this bucket: covid-eu, staging
 
 'covid-eu' folder used to storage the data airflow downloadfrom website
 
 'staging' folder used for data temp location in the dataflow pipeline
 
 Meanwhile, in this folder upload two files writen by python:
 
 'covid_composer_dataflow_dag.py' : dag file for airflow, which define the workflow
 
 'dataflow_etl_bigquery.py' : dataflow file for dataflow pipeline
 
 ![airflow6](https://user-images.githubusercontent.com/98153604/151390395-96840b0d-ba58-4bb8-aab7-544d2f1bf6b0.JPG)
 
 ## 4. Create a bigquery dataset
 
 ![bigquery datasets](https://user-images.githubusercontent.com/98153604/151402985-04bda7cb-7408-4f96-afeb-92fbd2d46462.JPG)

 ## 5. Setting Airflow variables in Airflow web UI
 
Go back to Composer to check the status of your environment.

Once your environment has been created, click the name of the environment (highcpu) to see its details.

On the Environment details you'll see information such as the Airflow web interface URL, Kubernetes Engine cluster ID, and a link to the DAGs folder, which is stored in your bucket.

![airflow11](https://user-images.githubusercontent.com/98153604/151392333-be81ef29-98c5-400a-9228-46921128f365.JPG)

Open Airflow web interface URL, setting Airflow variables. Select Admin > Variables from the Airflow menu bar, then Create.

![airflow5](https://user-images.githubusercontent.com/98153604/151392941-0a705cbf-f411-428c-aae4-b44f63bb9e2b.JPG)

## 6. Copy the DAG python file to Cloud Storage Dag folder

In step4, in the environment configration, we will find DAG folder path: 'gs://europe-central2-highcpu-816bf1da-bucket/dags'
In step3, we have already upload the dag python file 'covid_composer_dataflow_dag.py' in the google cloud storage

Run command line in cloud shell to copy dag python file to DAG folder:
    
    gsutil cp gs://t-osprey-337221-covid/covid_composer_dataflow_dag.py gs://europe-central2-highcpu-816bf1da-bucket/dags

After this in DAG folder we will see the Dag python file 'covid_composer_dataflow_dag.py' is in Dag folder

![airflow8](https://user-images.githubusercontent.com/98153604/151394951-0f9d11e4-6631-44e7-9144-a5d8cabbb35a.JPG)

After this The airflow start to run the whole work flow

The Dag file contant:

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
        
   In this Dag file, you will found 3 operators, which means the whole work flow can be 3 parts, the third the operator is 'BeamRunPythonPipelineOperator'
   This operater is function for run a insert dataflow job, thie dataflow job file is already upload in 'gs://t-osprey-337221-covid/dataflow_etl_bigquery.py'
   
   dataflow_etl_bigquery.py, the details of dataflow is :
 
        import apache_beam as beam
        import apache_beam.runners.interactive.interactive_beam as ib
        from apache_beam.runners.interactive.interactive_runner import InteractiveRunner
        from apache_beam.dataframe import convert
        #pandas
        from apache_beam.dataframe.transforms import DataframeTransform



        PROJECT='t-osprey-337221'
        BUCKET='t-osprey-337221-covid'

        """
        from apache_beam.io.gcp.internal.clients import bigquery

        table_spec_region = bigquery.TableReference(
            projectId='t-osprey-337221',
            datasetId='covid_eu',
            tableId='covid_region')

        table_spec_country = bigquery.TableReference(
            projectId='t-osprey-337221',
            datasetId='covid_eu',
            tableId='covid_country')
        """	
        # project-id:dataset_id.table_id
        table_spec_region = 't-osprey-337221:covid_eu.covid_region'
        table_spec_country = 't-osprey-337221:covid_eu.covid_country'


        # column_name:BIGQUERY_TYPE, ...
        table_schema_region = 'country:string, region_name:string, nuts_code:string, date:TIMESTAMP, rate_14_day_per_100k:float'
        table_schema_country = 'dateRep:string, cases:integer, deaths:integer, countriesAndTerritories:string, geoId:string, countryterritoryCode:string, popData2020:integer'


        def run():
            argv = [
              '--project={0}'.format(PROJECT),
              '--save_main_session',
              '--staging_location=gs://{0}/staging/'.format(BUCKET),
              '--temp_location=gs://{0}/staging/'.format(BUCKET),
              '--region=europe-north1',
              '--runner=DataflowRunner'
            ]
            with beam.Pipeline(argv=argv) as pipeline:
                # Create two deferred Beam DataFrames with the contents of our csv file.
                region_df = pipeline | 'Read region CSV' >> beam.dataframe.io.read_csv(r'gs://t-osprey-337221-covid/covid-eu/region.csv', usecols=[0,1,2,3,4])
                country_df = pipeline | 'Read country CSV' >> beam.dataframe.io.read_csv(r'gs://t-osprey-337221-covid/covid-eu/country.csv', usecols=[0,4,5,6,7,8,9])

                # Data cleaning
                region_df.fillna(value=0,inplace=True)
                region_df=region_df.astype({'country':'string', 'region_name':'string', 'nuts_code':'string', 'date':'datetime64', 'rate_14_day_per_100k':'float'})
                country_df=country_df.astype({'dateRep':'string', 'cases':'int', 'deaths':'int', 'countriesAndTerritories':'string', 'geoId':'string', 'countryterritoryCode':'string', 'popData2020':'int'})
                country_df['cases'].fillna(value=0, inplace=True)
                country_df['deaths'].fillna(value=0, inplace=True) 

                (
                  # Convert the Beam DataFrame to a PCollection.
                  convert.to_pcollection(region_df)

                  # We get named tuples, we can convert them to dictionaries like this.
                  | 'region To dictionaries' >> beam.Map(lambda x: dict(x._asdict()))

                  # save the elements to GCS.
                  |  'region save to bigquery' >> beam.io.WriteToBigQuery(
                                                                        table_spec_region,
                                                                        schema=table_schema_region,
                                                                        write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                                                                        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED)
                )
                (
                  # Convert the Beam DataFrame to a PCollection.
                  convert.to_pcollection(country_df)

                  # We get named tuples, we can convert them to dictionaries like this.
                  | 'country To dictionaries' >> beam.Map(lambda x: dict(x._asdict()))

                  # save the elements to GCS.
                  |  'country save to bigquery' >> beam.io.WriteToBigQuery(
                                                                        table_spec_country,
                                                                        schema=table_schema_country,
                                                                        write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                                                                        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED)
                )


        if __name__ == '__main__':
           run()
           
     
     This dataflow file writen by python, using beam structure.
     
   ## 7. Exploring DAG runs
   Open Airflow web interface:
   
   ![airflow2](https://user-images.githubusercontent.com/98153604/151399765-68857d63-577b-46df-9c42-85dfce09cceb.JPG)
    
   Open covid_composer_dataflow_dag
   
 ![airflow1](https://user-images.githubusercontent.com/98153604/151400286-1b02c3e1-1413-4e67-b6d6-5d8e83b05f0a.JPG)
   
 ![airflow15](https://user-images.githubusercontent.com/98153604/151400507-7caf7449-6137-4401-beef-eb9bb92e0d41.JPG)
   
   When this dag successful finished, go to Dataflow console, you will see a dataflow job create:
   
 ![airflow12](https://user-images.githubusercontent.com/98153604/151400951-7c259632-eab9-47bf-a240-30da9c39fa7f.JPG)
   
  Open this job:
  
  ![airflow13](https://user-images.githubusercontent.com/98153604/151401360-17b74312-4009-4d62-a726-c62b97ae02cf.JPG)
  
  ![airflow14](https://user-images.githubusercontent.com/98153604/151401410-ed4c26b6-70f3-4795-a47c-3fa8308c337b.JPG)
  
 ## 8. Check the Bigquery
 
 two new tables have been generate
 
 ![bigquery country](https://user-images.githubusercontent.com/98153604/151403206-92befa09-5508-4ca4-94c7-d51af98b29ce.JPG)
 
 ![bigquery region](https://user-images.githubusercontent.com/98153604/151403298-56d7711c-0709-4636-b1fa-1af0ab8fd01a.JPG)
 
 ## 9. Connect to Tableau
 
 ![Tableau](https://user-images.githubusercontent.com/98153604/151406640-8493c112-3a24-40e5-a979-5b7bfe9e9b0d.JPG)

 
 

 

  
  
  
  


  

   
   


    



   




 
 
 
 

 
 

 








