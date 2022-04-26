from airflow.decorators import task
from google.cloud import translate_v3 as translate
import logging, os

client = translate.TranslationServiceClient()
PROJECT_ID = os.getenv('PROJECT_ID', 'fasttrack-poc')
GLOSSARY_URI = f'gs://translation-glossary-{PROJECT_ID}/glossary.csv'

@task(task_id='upsert_glossary')
def upsert():
    # Supported language codes: https://cloud.google.com/translate/docs/languages
    source_lang_code = 'en'
    target_lang_code = 'fr'
    location = 'us-central1'  

    name = client.glossary_path(PROJECT_ID, location, 'glossary_v1')

    try:
        client.delete_glossary(name)
    except Exception as e:
        if e.message == 'Glossary not found.':
            logging.info('Deleting glossary failed', e)
        else:
            raise e

    language_codes_set = translate.types.Glossary.LanguageCodesSet(
        language_codes=[source_lang_code, target_lang_code]
    )

    gcs_source = translate.types.GcsSource(input_uri=GLOSSARY_URI)

    input_config = translate.types.GlossaryInputConfig(gcs_source=gcs_source)

    glossary = translate.types.Glossary(
        name=name, language_codes_set=language_codes_set, input_config=input_config
    )

    parent = f'projects/{PROJECT_ID}/locations/{location}'
    operation = client.create_glossary(parent=parent, glossary=glossary)
    

    result = operation.result(180)
    logging.info('Created: {}'.format(result.name))
    logging.info('Input Uri: {}'.format(result.input_config.gcs_source.input_uri))


