import abc

from .base_brick_processor import BaseBrickProcessor


class GenericBrickProcessor(BaseBrickProcessor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abc.abstractmethod
    def process(self, *args, **kwargs):
        pass
