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


