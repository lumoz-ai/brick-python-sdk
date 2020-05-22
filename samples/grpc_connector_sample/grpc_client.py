from time import time

from bricksdk.connectors.grpc.grpc_output_connector import GrpcOutputConnector
from protos import image_pb2

output_connector = GrpcOutputConnector("../../protos/image.proto")
output_connector.initialize()
output_connector.start()

image = image_pb2.Image(imageID=1, imageBytes=b"sdfasdf", imageWidth=256, imageHeight=256, numberOfChannels=3,
                        sentAt=time())
images = image_pb2.Images(images=[image])

response = output_connector.send(message=images)
print(response)
