# Covid-cases-in-EU-updated-daily-pipeline

![process](https://user-images.githubusercontent.com/98153604/151380489-f4fe3d0c-ca49-4da3-8df6-dff6ad94c9da.png)

## About the dataset
At the request of Member States, data on the daily number of new reported COVID-19 cases and deaths by EU/EEA country will be available to download from 11 March 2021 on European Centre for Disease Prevention and Control website (https://www.ecdc.europa.eu/en/covid-19/data). 

## About this project

In this project, I create an ETL batch data pipeline on google cloud platform by using Dataflow and Composer(AirFlow). The whole workflow covers two daily data download, data upload to Google cloud storage, data transform and cleaning by Dataflow and load data to bigquery. When data in Bigquery, we can analyze data using SQL in Bigquery and connect Tableau to Bigquery for data visulization and analysis.

The project contains follow steps:

1. Enable API used in this project:

(1) Enable Kubernetes Engine API 

![Kuberne API](https://user-images.githubusercontent.com/98153604/151383877-9e9cfc88-220c-4435-bf44-0e571f1290f4.JPG)

(2) Enable DataFlow API in this project

![dataflow API](https://user-images.githubusercontent.com/98153604/151384087-9136dd81-83fc-442e-b12c-a3137c8965ed.JPG)

(3) Enable Cloud Composer API

![composer API](https://user-images.githubusercontent.com/98153604/151384240-f0e80581-ce74-40b4-a7d8-2339e08fa4b5.JPG)






