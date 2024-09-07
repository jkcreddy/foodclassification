import os
from src.foodclassification.constants import *
from src.foodclassification.utils.common import read_yaml, create_directories
from src.foodclassification.entity.config_entity import DataIngestionConfig

class ConfigurationManager:
    def __init__(
            self,
            config_filepath = CONFIG_FILE_PATH,
            params_filepath = PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            object_key=config.object_key,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir,
            bucket_name=config.bucket_name,
            access_key=os.environ['AWS_ACCESS_KEY_ID'],
            secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            region=os.environ['AWS_DEFAULT_REGION']
        )

        return data_ingestion_config