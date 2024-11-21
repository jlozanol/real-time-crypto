import os

from dotenv import find_dotenv, load_dotenv

# load my .env file variables as environment variables so I can access them
# with os.environ[] statements
load_dotenv(find_dotenv())

kafka_broker_address = os.environ['KAFKA_BROKER_ADDRESS']
kafka_topic_name = 'trade'
product_id = 'BTC/USD'
