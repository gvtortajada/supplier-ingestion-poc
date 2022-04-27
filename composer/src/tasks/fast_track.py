from airflow.decorators import task
import pandas as pd
import numpy as np
import time, os, logging, traceback, math
from datetime import datetime
from google.cloud import (
    bigquery, 
    storage
)
from tasks.schemas import get_fasttrack_column, get_supplier_schema
from tasks.utils import (
    AssetType,
    gcs_move_file,
    transfert_assets,
    translate_text
)

bq_client = bigquery.Client()
view_id = 'fasttract.suppliers-catalogs'
table_id = 'fasttract.suppliers-catalogs-raw'
gcs_client = storage.Client()
French_description_mapping = 'DescriptionFrench'
English_description_mapping = 'DescriptionEnglish'
image_mapping = 'Image'
French_manual_mapping = 'SpecsFR'
English_manual_mapping = 'SpecsEN'
mandatory_columns = ['SupplierFileName','ManufacturerProductNumber','VendorNumber', 'VendorName', 'Brand', 'DescriptionEnglish']
processing_chunk_size = 100
PROJECT_ID = os.getenv('PROJECT_ID', 'fasttrack-poc')


@task(task_id="load_supplier_files", retries=1)
def load_supplier_files(mapping):
    global_start = time.time()
    mapping_df = pd.read_json(mapping)
    for blob in gcs_client.list_blobs(f'supplier-catalogs-import-{PROJECT_ID}'):
        try:
            logging.info(f'loading file: {blob.name}')
            start_date = datetime.now()
            # move file to in progress bucket
            in_progress_state(blob)

            # load supplier file from GCS
            supplier_df, supplier_mapping_df, supplier_ext, supplier_name = load_supplier_file(blob, mapping_df)

            # mapping to fast track schema
            supplier_df = apply_fast_track_schema(supplier_mapping_df, supplier_df)

            # validate dataframe
            is_valid, supplier_df = validate(supplier_df)

            if not is_valid:
                logging.error('Found empty elements in mandatory columns: {mandatory_columns_with_empty_val}')
                in_error_state(blob, supplier_name, supplier_ext)
            else:
                # load supplier data from bigquery
                now = time.time()
                df_bq = load_existing_data_from_bigquery(supplier_name)

                # remove existing supplier item in bigquery
                if df_bq.size > 0:
                    #remove duplicates
                    supplier_df = pd.concat([supplier_df, df_bq])\
                            .drop_duplicates(keep=False, subset=get_fasttrack_column())
                    #when differences keep data from new files
                    supplier_df = supplier_df.drop_duplicates(keep='first', subset=['ManufacturerProductNumber'])

                if supplier_df.size > 0:
                    # devide the work in chunks
                    nb_chunks = math.ceil(len(supplier_df.index) / processing_chunk_size)
                    chunks = np.array_split(supplier_df, nb_chunks)
                    processed_chunks = 0
                    for chunk in chunks:
                        if chunk.size > 0:
                            start = time.time()
                            # translations
                            chunk = translate(chunk)

                            # images and manuals
                            for row in chunk.iterrows():
                                product_id = row[1]['ManufacturerProductNumber']            
                                # Get image
                                download_asset(row[1][image_mapping], supplier_name, AssetType.IMAGES, product_id)
                                # Get manuals
                                for url in [row[1][French_manual_mapping], row[1][English_manual_mapping]]:
                                    download_asset(url, supplier_name, AssetType.MANUAL, product_id)

                            # load dataframne to Bigquery
                            load_to_bigquery(chunk, start_date)
                            processed_chunks+=1
                            logging.info(f'{blob.name} completion: {processed_chunks} over {nb_chunks}')
                            now = time.time()
                            logging.info(f'chunk duration:{round(now - start,3)}s  total duration:{round(now - global_start,3)}s')
                
                # move file to done bucket
                in_complete_state(blob, supplier_name, supplier_ext)
        except Exception as e:
            # move file to failed bucket
            in_error_state(blob, supplier_name, supplier_ext, e)
            print(traceback.print_exc())


def load_supplier_file(blob, mapping):
    supplier_name = blob.name.rsplit('.', 1)[0]
    supplier_ext = blob.name.rsplit('.', 1)[1]
    supplier_name_search = supplier_name.replace('(','\(')
    supplier_name_search = supplier_name_search.replace(')','\)')
    supplier_mapping_df = mapping[mapping['SupplierFileName'].str.contains(supplier_name_search)]
    # excel file to dataframe
    now = time.time()
    supplier_df = pd.read_excel(
        f'gs://supplier-catalogs-in-progress-{PROJECT_ID}/{blob.name}',
        engine='openpyxl',
        dtype = str
    )
    supplier_df.columns = supplier_df.columns.str.strip()
    logging.info(f'Loading supplier file in {round(time.time() - now,3)}s')
    return supplier_df, supplier_mapping_df, supplier_ext, supplier_name


def apply_fast_track_schema(supplier_mapping_df, supplier_df):
    filter=[]
    empty_columns=[]
    for index, value in supplier_mapping_df.iloc[0].items():
        if pd.isna(value) or not value in supplier_df.columns:
            empty_columns.append({'index':index, 'value': None if pd.isna(value) else str(value)})
        else:
            filter.append({'mapping_key':index, 'supplier_key':value})
    supplier_df = supplier_df.filter([e['supplier_key'] for e in filter])
    supplier_df.columns = [e['mapping_key'] for e in filter]
    for e in empty_columns:
        supplier_df[e['index']]=e['value']
    return supplier_df

def validate(supplier_df):
    mandatory_column_empty_val_found = False
    for column in mandatory_columns:
        mandatory_column_empty_val_found = \
            mandatory_column_empty_val_found or supplier_df[column].isnull().values.any()
    return not mandatory_column_empty_val_found, supplier_df


def load_existing_data_from_bigquery(supplier_name):
    now = time.time()
    df_bq = (
        bq_client.query(
            f'''
            SELECT * FROM `{PROJECT_ID}.{view_id}` 
            WHERE SupplierFileName = '{supplier_name}'
            '''
        ).result()
        .to_dataframe(create_bqstorage_client=True)
    )
    logging.info(f'Loading existing supplier data in {round(time.time() - now,3)}s')
    return df_bq

def translate(df):
    english_descriptions = df[English_description_mapping].tolist()
    translation_response = translate_text(english_descriptions)
    translation_response = [t.translated_text for t in translation_response]
    df[French_description_mapping] = pd.Series(translation_response).values
    return df


def download_asset(url, supplier_name, asset_type, product_id):
    if url and not pd.isna(url):
        try:
            transfert_assets(
                supplier_name, 
                url,
                gcs_client, 
                asset_type
            )
        except Exception as ex:
            logging.info(f'fail to download {asset_type} for {supplier_name} - {product_id}: {ex}')


def load_to_bigquery(df, start_date):
    df['creationDate']=start_date
    job_config = bigquery.LoadJobConfig(
        schema = get_supplier_schema(),
        autodetect=False,
        write_disposition="WRITE_APPEND",
    ) 
    job = bq_client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()


def in_progress_state(blob):
    gcs_move_file(
        f'supplier-catalogs-import-{PROJECT_ID}',
        blob.name,
        f'supplier-catalogs-in-progress-{PROJECT_ID}',
        blob.name,
        gcs_client
    )

def in_complete_state(blob, supplier_name, supplier_ext):
    gcs_move_file(
        f'supplier-catalogs-in-progress-{PROJECT_ID}',
        blob.name,
        f'supplier-catalogs-completed-{PROJECT_ID}',
        f'{supplier_name}-{datetime.now()}.{supplier_ext}',
        gcs_client
    )

def in_error_state(blob, supplier_name, supplier_ext, exception):
    logging.error(f'Processing failed for file: {blob.name}', exception)
    gcs_move_file(
        f'supplier-catalogs-in-progress-{PROJECT_ID}',
        blob.name,
        f'supplier-catalogs-error-{PROJECT_ID}',
        f'{supplier_name}-{datetime.now()}.{supplier_ext}',
        gcs_client
    )