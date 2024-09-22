from foodclassification.config.configuration import ConfigurationManager
from foodclassification.components.evaluation import Evaluation
from foodclassification import logger


STAGE_NAME = "Evaluation Stage"

class EvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            val_config = config.get_validation_config()
            evaluation = Evaluation(val_config)
            evaluation.evaluation()
            evaluation.save_score()

        except Exception as e:
            pass

if __name__== '__main__':
    try:
        logger.info(f"***************************")
        logger.info(f">>>>>>>> stage {STAGE_NAME} started <<<<<<<")
        obj = EvaluationPipeline()
        obj.main()
        logger.info(f">>>>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx========x")
    except Exception as e:
        logger.exception(e)
        raise e