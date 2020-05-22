from google.protobuf.pyext._message import RepeatedCompositeContainer


class ProtoCombiner:

    def __init__(self, input_protos=None, output_proto=None):
        self.input_protos = input_protos
        self.output_proto = output_proto

    def combine(self, input_protos=None, output_proto=None):
        self.input_protos = input_protos if input_protos else self.input_protos
        self.output_proto = output_proto if output_proto else self.output_proto
        if self.input_protos and self.output_proto:
            try:
                for input_proto in self.input_protos:
                    self.validate_and_combine(input_proto)
                return self.output_proto
            except ValueError as ve:
                print(ve)

    def validate_and_combine(self, input_proto):
        for variable_name, object in self.output_proto.DESCRIPTOR.fields_by_name.items():
            # print(variable_name, type(getattr(images, variable_name)),getattr(images, variable_name))
            if type(getattr(self.output_proto, variable_name)) is RepeatedCompositeContainer:
                if type(getattr(self.output_proto, variable_name)[0]) is type(input_proto):
                    getattr(self.output_proto, variable_name).append(input_proto)
                    return
            elif type(getattr(self.output_proto, variable_name)) is type(input_proto):
                getattr(self.output_proto, variable_name).CopyFrom(input_proto)
                return
        raise Exception("Cannot combine the protos")
