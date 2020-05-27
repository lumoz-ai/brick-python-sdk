import requests
from google.protobuf.json_format import MessageToDict


class ArtifactConfig:

    def __init__(self):
        self.host: str = ""
        self.port: str = ""
        self.endpoint: str = ""


class ArtifactPublisher:

    def __init__(self, artifact_config: ArtifactConfig):
        self.artifact_config = artifact_config
        self.url = str(self.artifact_config.host) + ':' + str(self.artifact_config.port) + '/' + str(
            self.artifact_config.endpoint)

    def publish(self, proto_object):
        proto_dict = self.create_json_object(proto_object)
        requests.post(self.url, data = proto_dict)

    @staticmethod
    def create_json_object(proto_object):
        return MessageToDict(proto_object)
