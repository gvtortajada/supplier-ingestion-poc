from enum import Enum
from google.cloud import translate_v3 as translate
import requests, os, mimetypes, logging, validators
from retrying import retry
from requests.adapters import HTTPAdapter
from urllib3 import Retry

class AssetType(Enum):
    IMAGES = 1
    MANUAL = 2

translate_client = translate.TranslationServiceClient()
PROJECT_ID = os.getenv('PROJECT_ID', 'fasttrack-poc')
retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=['HEAD', 'GET', 'OPTIONS']
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount('https://', adapter)
http.mount('http://', adapter)

glossary = translate_client.glossary_path(
    PROJECT_ID, 'us-central1', 'glossary_v1'  # The location of the glossary
)

glossary_config = translate.types.TranslateTextGlossaryConfig(glossary=glossary)

def retry_on_exception(exception):
    logging.error(f'retrying on exception: {exception}')
    return True

def gcs_move_file(bucket_name, blob_name, new_bucket_name, new_blob_name, storage_client):
    source_bucket = storage_client.get_bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.get_bucket(new_bucket_name)
    # copy to new destination
    source_bucket.copy_blob(
        source_blob, destination_bucket, new_blob_name)
    # delete in old destination
    source_blob.delete()
    print(f'File moved from {source_blob} to {new_blob_name}')

@retry(
    stop_max_attempt_number=3,
    retry_on_exception=retry_on_exception,
    wait_exponential_multiplier=1000, 
    wait_exponential_max=10000
)
def translate_text(text):
    location = 'us-central1'
    parent = f'projects/{PROJECT_ID}/locations/{location}'
    response = translate_client.translate_text(
        parent=parent,
        contents=text,
        source_language_code='en',
        target_language_code='fr',
        mime_type='text/plain',
        glossary_config=glossary_config
    )
    return response.glossary_translations

@retry(
    stop_max_attempt_number=3,
    retry_on_exception=retry_on_exception,
    wait_exponential_multiplier=1000, 
    wait_exponential_max=10000
)
def transfert_assets(supplier, url, storage_client, asset_type):
    logging.debug(f'transfering asset: {url}')
    if validators.url(url) is True: # if is is a valid url
        images_bucket_name = f'supplier-product-images-{PROJECT_ID}'
        manual_bucket_name = f'supplier-product-manual-{PROJECT_ID}'
        filename = url.rsplit('/', 1)[-1]
        target_bucket_name = images_bucket_name if asset_type is AssetType.IMAGES else manual_bucket_name
        target_bucket = storage_client.get_bucket(target_bucket_name)
        content = http.get(url).content
        target_blob = target_bucket.blob(supplier + '/' + filename)
        content_type = mimetypes.guess_type(filename)
        # Get the content type for being able to visualize it in the browser
        if content_type:
            target_blob.upload_from_string(content, content_type=content_type[0])
        else:
            target_blob.upload_from_string(content)


