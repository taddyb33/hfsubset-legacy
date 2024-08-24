import os
from pathlib import Path

from pydantic import ConfigDict
from pydantic_settings import BaseSettings

from src.hfsubset.app.core.utils import find_repo_root


class Settings(BaseSettings):
    api_v1_str: str = "/api/v1"
    subset_output_path : Path = "/app/data"
    project_name: str = "Hfsubsetter (v20.1)"
    network_file: str = "/app/gpkg/conus_net.parquet"