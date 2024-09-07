import os
import boto3
import yaml
from pathlib import Path
import urllib.request as request
from box.exceptions import BoxValueError
import zipfile
from src.foodclassification import logger
from src.foodclassification.utils.common import get_size
from src.foodclassification.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            s3 = boto3.client(
                's3',
                aws_access_key_id=self.config.access_key,
                aws_secret_access_key=self.config.secret_access_key,
                region_name=self.config.region)

            bucket_name = self.config.bucket_name
            s3_file_key = self.config.object_key
            local_file_path = self.config.local_data_file

            try:
                s3.download_file(bucket_name, s3_file_key, local_file_path)
                logger.info(f"File '{s3_file_key}' downloaded to '{local_file_path}'.")
            except BoxValueError:
                raise ValueError("unable to download file from s3")
        else:
            logger.info(f"file already present of size: {get_size(Path(self.config.local_data_file))}")

    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)