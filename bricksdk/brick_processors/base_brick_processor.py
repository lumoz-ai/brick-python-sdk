import abc


class BaseBrickProcessor(abc.ABC):

    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def process(self, *args, **kwargs):
        pass
