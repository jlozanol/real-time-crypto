from datetime import timedelta

from loguru import logger
from quixstreams import Application

from src.config import config


def trade_to_ohlc(
	kafka_input_topic: str,
	kafka_output_topic: str,
	kafka_broker_address: str,
	ohlc_window_seconds: int,
) -> None:
	"""
	Reads trades from the Kafka Input topic,
	aggregates them into OHLC candles using the specified window in
	`ohlc_window_seconds` and saves the data into another Kafka topic.

	Args:
	    kafka_input_topic (str): Kafka topic to read trade data from
	    kafka_output_topic (str): Kafka topic to write OHLC data to
	    kafka_broker_address (str): Kafka broker address
	    ohlc_window_seconds (int): Window size in seconds for OHLC aggregation

	Returns:
	    None
	"""

	# Handling low-level communication with Kafka
	app = Application(
		broker_address=kafka_broker_address, consumer_group='trade_to_ohlc'
	)

	# Specify input and output topics
	input_topic = app.topic(name=kafka_input_topic, value_serializer='json')
	output_topic = app.topic(name=kafka_output_topic, value_serializer='json')

	# Create StreamingDataFrame and connect it to the input topic
	# to apply transformations to the incoming data
	sdf = app.dataframe(topic=input_topic)

	# Define initializer function for transformation
	def init_ohlc_candle(value: dict) -> dict:
		"""
		Initialize the OHLC candle with the first trade
		"""
		return {
			'open': value['price'],
			'high': value['price'],
			'low': value['price'],
			'close': value['price'],
			'product_id': value['product_id'],
		}

	# Define reducer function to update the data of the OHLC
	def update_ohlc_candle(ohlc_candle: dict, trade: dict) -> dict:
		"""
		Update the OHLC candle with the new trade and return the updated candle

		Args:
		    ohlc_candle (dict): The current OHLC candle
		    trade (dict): The incoming trade

		Returns:
		    dict: The updated OHLC candle
		"""

		return {
			'open': ohlc_candle['open'],
			'high': max(ohlc_candle['high'], trade['price']),
			'low': min(ohlc_candle['low'], trade['price']),
			'close': trade['price'],
			'product_id': trade['product_id'],
		}

	# Apply transformations to the incoming data
	sdf = sdf.tumbling_window(duration_ms=timedelta(seconds=ohlc_window_seconds))
	sdf = sdf.reduce(reducer=update_ohlc_candle, initializer=init_ohlc_candle).final()

	# Extract the open, high, low and close prices from the value key
	sdf['open'] = sdf['value']['open']
	sdf['high'] = sdf['value']['high']
	sdf['low'] = sdf['value']['low']
	sdf['close'] = sdf['value']['close']
	sdf['product_id'] = sdf['value']['product_id']
	sdf['timestamp'] = sdf['end']

	sdf = sdf[['timestamp', 'product_id', 'open', 'high', 'low', 'close']]

	sdf = sdf.update(logger.info)

	# Publish data to the output topic
	sdf = sdf.to_topic(output_topic)

	# Run the pipeline
	app.run(sdf)


if __name__ == '__main__':
	trade_to_ohlc(
		kafka_input_topic=config.kafka_input_topic,
		kafka_output_topic=config.kafka_output_topic,
		kafka_broker_address=config.kafka_broker_address,
		ohlc_window_seconds=config.ohlc_window_seconds,
	)
