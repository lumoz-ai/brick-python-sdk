import re
from ..utils import Singleton


class Configuration(metaclass=Singleton):

    def __init__(self, *args, **kwargs):
        pass

    def load(self, json: dict):
        try:
            for key, value in json.items():
                if type(value) is dict:
                    value = self._build(key, value)
                self.__setattr__(self._to_snake(key), value)
            return self
        except:
            pass

    def _build(self, name, attributes: dict):
        configuration_class = type(self._to_camel(name, True), (Configuration,), {})
        configuration_object = configuration_class()
        for key, value in attributes.items():
            if type(value) is dict:
                value = self._build(key, value)
            configuration_object.__setattr__(self._to_snake(key), value)
        return configuration_object

    def update(self, json):
        pass

    def get_variables(self):
        variable_list = {}
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                key = key[1:]
            variable_list[key] = value
        return variable_list

    def __repr__(self):
        return str({"[{}]".format(self.__class__.__name__): self.__dict__})

    def _to_snake(self, variable_name):
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', variable_name).lower()
        return name

    def _to_camel(self, variable_name, capitalize=False):
        variable_name = variable_name.split("_")
        variable_name = [name.capitalize() if i > 0 else name for i, name in enumerate(variable_name)]
        variable_name = "".join(variable_name)
        if capitalize:
            variable_name = variable_name[0].capitalize() + variable_name[1:]
        return variable_name

    def get_class_reference(self, class_name, values):
        class_reference = type(class_name, (Configuration,), values)
        return class_reference
