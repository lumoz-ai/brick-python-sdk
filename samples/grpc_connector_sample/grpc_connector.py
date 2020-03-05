import json
from time import time

from bricksdk.configurations import Configuration
from bricksdk.connectors import get_connector
from protos import image_pb2

config = Configuration()
config.load(json=json.load(open("sample_configuration.json", "r")))


class BrickProcessor:

    def process(self, request, context):
        print(request)
        result = image_pb2.ImageClassificationResult(image=request.images[0], label="man", confidence=76.56,
                                                     sentAt=time())
        results = image_pb2.ImageClassificationResults(imageClassificationResults=[result])
        print(results)
        return results


# class config:
#     input_connector_type = 1


connector = get_connector(config=config, brick_processor=BrickProcessor(), input_proto_file_path="protos/image.proto",
                          output_proto_file_path="protos/image.proto")

connector.start()

image = image_pb2.Image(imageID=1, imageBytes=b"sdfasdf", imageWidth=256, imageHeight=256, numberOfChannels=3,
                        sentAt=time())
images = image_pb2.Images(images=[image])

connector.output_connector.send(images)
