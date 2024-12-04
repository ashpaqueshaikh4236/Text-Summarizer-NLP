from textsummarizer.config.configuraion import ConfigurationManager
from textsummarizer.components.data_ingestion  import DataIngestion
from textsummarizer.logging import logger


STAGE_NAME = "Data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass
        
    def main(self):
        config = ConfigurationManager()
        data_ingetsion_config = config.get_data_ingestion_config()
        data_ingetsion = DataIngestion(config=data_ingetsion_config)
        data_ingetsion.download_file()
        data_ingetsion.extract_zip_file()


if __name__ == '__main__':
    try:
        logger.info(f" <<<<<----- {STAGE_NAME} started ----->>>>> ")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f" ----->>>>> {STAGE_NAME} completed <<<<<----- ")
    except Exception as e:
        logger.exception(e)
        raise e