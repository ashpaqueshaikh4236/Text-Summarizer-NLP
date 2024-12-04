from textsummarizer.config.configuraion import ConfigurationManager
from textsummarizer.components.data_transformation  import DataTransformation
from textsummarizer.logging import logger


STAGE_NAME = "Data Transformation Stage"

class DataTransformtionTrainingPipeline:
    def __init__(self):
        pass
        
    def main(self):
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformation(config=data_transformation_config)
        data_transformation.convert()


if __name__ == '__main__':
    try:
        logger.info(f" <<<<<----- {STAGE_NAME} started ----->>>>> ")
        obj = DataTransformtionTrainingPipeline()
        obj.main()
        logger.info(f" ----->>>>> {STAGE_NAME} completed <<<<<----- ")
    except Exception as e:
        logger.exception(e)
        raise e