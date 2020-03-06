from . import connector_types
from .connector_types import INPUT_CONNECTORS, OUTPUT_CONNECTORS, CONNECTORS


def get_connector(config, brick_processor, *args, **kwargs):
    assert config.brick.input_connector_type is not None
    connector = CONNECTORS[config.brick.input_connector_type](config, brick_processor, *args, **kwargs)
    connector.initialize()
    return connector


def get_input_connector(config, brick_processor, *args, **kwargs):
    assert config.brick.input_connector_type is not None
    input_connector = INPUT_CONNECTORS[config.brick.input_connector_type](
        *args, config=config, brick_processor=brick_processor, **kwargs
    )
    input_connector.initialize()
    return input_connector


def get_output_connector(config, *args, **kwargs):
    assert config.brick.input_connector_type is not None
    output_connector = OUTPUT_CONNECTORS[config.brick.output_connector_type](*args, config=config, **kwargs)
    output_connector.initialize()
    return output_connector
