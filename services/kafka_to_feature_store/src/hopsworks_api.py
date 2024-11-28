from typing import Dict

import hopsworks
import pandas as pd

from src.config import config


def push_data_to_feature_store(
	feature_group_name: str, feature_group_version: int, data: Dict
) -> None:
	"""
	Pushes the given `data` to the feature store writing it to the feature group
	`feature_group_name` and version `feature_group_version`.

	Args:
	    feature_group_name (str): The name of the feature group to write to.
	    feature_group_version (int): The version of the feature group to write to.
	    data (dict): The data to write to the feature store.

	Returns:
	    None
	"""

	# Authenticate with Hopsworks API
	project = hopsworks.login(
		project=config.hopsworks_project_name, api_key_value=config.hopsworks_api_key
	)

	# Get the feature store
	feature_store = project.get_feature_store()

	# Create or get the feture group where the feature data will be saved to
	ohlc_feature_group = feature_store.get_or_create_feature_group(
		name=feature_group_name,
		version=feature_group_version,
		description='OHLC data coming from Kraken API',
		primary_key=['product_id', 'timestamp'],
		event_time='timestamp',
		online_enabled=True,
	)

	# Transform the `data` (Dict) into a pandas df
	data = pd.DataFrame([data])

	# Write the data to the feature group
	ohlc_feature_group.insert(data)
