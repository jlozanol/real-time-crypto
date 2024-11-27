import hopsworks

def push_data_to_feature_store(
        feature_group_name: str,
        feature_group_version: int,
        data: dict
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

    project = hopsworks.login(
        project='',
        api_key_value=
    )