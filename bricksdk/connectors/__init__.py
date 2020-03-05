from . import connector_types
from .connector_types import CONNECTORS


def get_connector(config, brick_processor, *args, **kwargs):
    assert config.brick.input_connector_type is not None
    connector = CONNECTORS[config.brick.input_connector_type](config, brick_processor, *args, **kwargs)
    connector.initialize()
    return connector
