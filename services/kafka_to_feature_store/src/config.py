import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

# load my .env file variables as environment variables so I can access them
# with os.environ[] statements
load_dotenv(find_dotenv())


class Config(BaseSettings):
	hopsworks_api_key: str = os.environ['HOPSWORKS_API_KEY']
	hopsworks_project_name: str = os.environ['HOPSWORKS_PROJECT_NAME']
	kafka_broker_address: str = os.environ['KAFKA_BROKER_ADDRESS']
	kafka_topic: str = 'ohlc'
	feature_group_name: str = 'ohlc_feature_group'
	feature_group_version: int = 1


config = Config()
