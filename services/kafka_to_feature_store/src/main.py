import json

from loguru import logger
from quixstreams import Application

from src.config import config
from src.hopsworks_api import push_data_to_feature_store


def kafka_to_feature_store(
        kafka_topic: str,
        kafka_broker_address: str,
        feature_group_name: str,
        feature_group_version: int
) -> None:
    """
    Reads `ohlc` data from the Kafka topic and writes it to the feature store.
    It writes the data to the feature group specified by
    `feature_group_name` and `feature_group_version`.

    Args:
        kafka_topic (str): The Kafka topic to read from.
        kafka_broker_address (str): The address of the Kafka broker.
        feature_group_name (str): The name of the fature group to write to.
        feature_group_version (int): The version of the feature group to write to.

    Returns:
        None
    """

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group='kafka_to_feature_store'
    )

    # Create a consumer and start a pooling loop
    with app.get_consumer() as consumer:
        consumer.subscribe(topics=[kafka_topic])

        while True:
            msg = consumer.poll(1)
            if msg is None:
                continue

            elif msg.error():
                logger.error('Kafka error: ', msg.error())
                continue
            
            # Send data to the feature store 
            else:
                # Parse the message from Kafka into a dictionary
                ohlc = json.loads(msg.value().decode('utf-8'))

                logger.debug(f'Received message: {ohlc}')

                # Write the data into the feature store
                push_data_to_feature_store(
                    feature_group_name=feature_group_name,
                    feature_group_version=feature_group_version,
                    data=ohlc
                )

            # Store the offset of the processed message on the Consumer
            # for the auto-commit mechanism.
            # It will send it to Kafka in the background.
            # Storing offset only after the message is processed enables
            # at-least-once delivery guarantees.
            consumer.store_offsets(message=msg)


if __name__ == '__main__':
    kafka_to_feature_store(
        kafka_topic=config.kafka_topic,
        kafka_broker_address=config.kafka_broker_address,
        feature_group_name=config.feature_group_name,
        feature_group_version=config.feature_group_version
    )