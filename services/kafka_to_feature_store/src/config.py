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
	kafka_topic: str = os.environ['KAFKA_TOPIC']
	feature_group_name: str = os.environ['FEATURE_GROUP_NAME']
	feature_group_version: int = os.environ['FEATURE_GROUP_VERSION']


config = Config()
