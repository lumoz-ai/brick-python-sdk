import abc


class BaseRunner(abc.ABC):

    def __init__(self, json_graph=None, *args, **kwargs):
        self.json_graph = json_graph

    @abc.abstractmethod
    def generate_dependency_graph(self, json_graph=None):
        pass

    @abc.abstractmethod
    def execute_graph(self, *args, **kwargs):
        pass
