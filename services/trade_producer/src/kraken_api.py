import json
from typing import Dict, List

from loguru import logger
from websocket import create_connection


class KrakenWebsocketTradeAPI:
	URL = 'wss://ws.kraken.com/v2'

	def __init__(self, product_id: str):
		self.product_id = product_id

		# establish the connection to the Kraken websocket API
		self._ws = create_connection(self.URL)
		logger.info('Connection established...')

		#  subscribe to the trades for the given 'product_id'
		self._subscribe(product_id)

	def _subscribe(self, product_id: str):
		"""
		Establishing connection to the Kraken websocket API and subscribe to the trades for the given 'product_id'.
		"""
		logger.info(f'Subscribing to trades for {product_id}')

		# Subscribing to the trades for the given 'product_id'
		msg = {
			'method': 'subscribe',
			'params': {
				'channel': 'trade',
				'symbol': [
					product_id,
				],
				'snapshot': False,
			},
		}
		self._ws.send(json.dumps(msg))
		logger.info('Subscription successful!')

		# dumping first 2 messages from the websocket, it is not trade data
		_ = self._ws.recv()
		_ = self._ws.recv()

	def get_trades(self) -> List[Dict]:
		message = self._ws.recv()

		if 'heartbeat' in message:
			# when I get a heartbeat, return an empty list
			return []

		# parse the message string as a dictionary
		message = json.loads(message)

		# extract data from the message['data'] field
		trades = []
		for trade in message['data']:
			trades.append(
				{
					'product_id': self.product_id,
					'price': trade['price'],
					'volume': trade['qty'],
					'timestamp': trade['timestamp'],
				}
			)

		return trades
