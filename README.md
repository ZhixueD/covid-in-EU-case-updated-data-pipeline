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
4. Setting Airflow variables in Airflow web UI
5. Copy the DAG python file to Cloud Storage Dag folder

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
 
 ## 4. Setting Airflow variables in Airflow web UI
 
Go back to Composer to check the status of your environment.

Once your environment has been created, click the name of the environment (highcpu) to see its details.

On the Environment details you'll see information such as the Airflow web interface URL, Kubernetes Engine cluster ID, and a link to the DAGs folder, which is stored in your bucket.

![airflow11](https://user-images.githubusercontent.com/98153604/151392333-be81ef29-98c5-400a-9228-46921128f365.JPG)

Open Airflow web interface URL, setting Airflow variables. Select Admin > Variables from the Airflow menu bar, then Create.

![airflow5](https://user-images.githubusercontent.com/98153604/151392941-0a705cbf-f411-428c-aae4-b44f63bb9e2b.JPG)

## 5. Copy the DAG python file to Cloud Storage Dag folder

In step4, in the environment configration, we will find DAG folder path: 'gs://europe-central2-highcpu-816bf1da-bucket/dags'
In step3, we have already upload the dag python file 'covid_composer_dataflow_dag.py' in the google cloud storage

Run command line in cloud shell to copy dag python file to DAG folder:
    
    gsutil cp gs://t-osprey-337221-covid/covid_composer_dataflow_dag.py gs://europe-central2-highcpu-816bf1da-bucket/dags

After this in DAG folder we will see the Dag python file 'covid_composer_dataflow_dag.py' is in Dag folder

![airflow8](https://user-images.githubusercontent.com/98153604/151394951-0f9d11e4-6631-44e7-9144-a5d8cabbb35a.JPG)




 
 
 
 

 
 

 








