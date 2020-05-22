from .grpc.grpc_input_connector import GrpcInputConnector
from .grpc.grpc_output_connector import GrpcOutputConnector
from .grpc import GrpcConnector

GRPC_CONNECTOR = 1

CONNECTORS = {
    GRPC_CONNECTOR: GrpcConnector
}

INPUT_CONNECTORS = {
    GRPC_CONNECTOR: GrpcInputConnector
}

OUTPUT_CONNECTORS = {
    GRPC_CONNECTOR: GrpcOutputConnector
}
