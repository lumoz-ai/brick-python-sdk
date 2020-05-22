from time import time

from bricksdk.connectors.grpc.grpc_input_connector import GrpcInputConnector
from protos import image_pb2


class BrickProcessor:

    def process(self, request, context):
        print(request)
        result = image_pb2.ImageClassificationResult(image=request.images[0], label="man", confidence=76.56,
                                                     sentAt=time())
        results = image_pb2.ImageClassificationResults(imageClassificationResults=[result])
        print(results)
        return results


input_connector = GrpcInputConnector("../../protos/image.proto", None,
                                     brick_processor=BrickProcessor())

input_connector.initialize()
input_connector.start()
