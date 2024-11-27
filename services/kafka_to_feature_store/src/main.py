from quixstreams import Application
import json
from loguru import logger

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

                # Write the data into the feature store
                push_data_to_feature_store(
                    feature_group_name=feature_group_name,
                    feature_group_version=feature_group_version,
                    data=ohlc
                )

            breakpoint()

if __name__ == '__main__':
    kafka_to_feature_store(
        kafka_topic='ohlc',
        kafka_broker_address='localhost:19092',
        feature_group_name='ohlc_feature_group',
        feature_group_version=1
    )