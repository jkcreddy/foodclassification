from foodclassification.config.configuration import ConfigurationManager
from foodclassification.components.prepare_base_model import PrepareBaseModel
from foodclassification import logger
import ssl
import urllib3

STAGE_NAME = 'Prepare base model'

class PrepareBaseModelTrainingPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        #context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        #context.check_hostname = False
        #context.verify_mode = ssl.CERT_NONE
    
        # Use the context with the urllib3 PoolManager
        #http = urllib3.PoolManager(ssl_context=context)

        #vgg16 = tf.keras.applications.VGG16(weights='imagenet', include_top=False)
        config = ConfigurationManager()
        prepare_base_model_config = config.get_prepare_base_model_config()
        prepare_base_model = PrepareBaseModel(config=prepare_base_model_config)
        prepare_base_model.get_base_model()
        prepare_base_model.update_base_model()

if __name__ == '__main__':
    try:
        logger.info(f"***************************")
        logger.info(f">>>>>>>> stage {STAGE_NAME} started <<<<<<<<<<")
        obj = PrepareBaseModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx===============x")
    except Exception as e:
        logger.exception(e)
        raise e
