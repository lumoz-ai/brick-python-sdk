import abc

import _thread


class BaseConnector(abc.ABC):

    def __init__(self, *args, **kwargs):
        self.input_connector = None
        self.output_connector = None

    @abc.abstractmethod
    def initialize_input_connector(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def initialize_output_connector(self, *args, **kwargs):
        pass

    def initialize(self, *args, **kwargs):
        self.initialize_input_connector(*args, **kwargs)
        self.initialize_output_connector(*args, **kwargs)

    def get_input_connector(self):
        return self.input_connector

    def get_output_connector(self):
        return self.output_connector

    def start_input_connector(self, *args, **kwargs):
        self.input_connector.start(*args, **kwargs)

    def start_output_connector(self, *args, **kwargs):
        self.output_connector.start(*args, **kwargs)

    def start(self, *args, **kwargs):
        _thread.start_new_thread(self.start_input_connector, (args, kwargs))
        _thread.start_new_thread(self.start_output_connector, (args, kwargs))


class BaseInputConnector(abc.ABC):

    def __init__(self):
        pass

    @abc.abstractmethod
    def initialize(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def listen(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def start(self, *args, **kwargs):
        pass


class BaseOutputConnector(abc.ABC):

    def __init__(self):
        pass

    @abc.abstractmethod
    def initialize(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def send(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def start(self, *args, **kwargs):
        pass
