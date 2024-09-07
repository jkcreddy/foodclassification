from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    object_key: Path
    local_data_file: Path
    unzip_dir: Path
    bucket_name: str
    access_key: str
    secret_access_key: str
    region: str