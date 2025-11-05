import abc
from random import randint


class BaseBrickRunner(abc.ABC):

    def __init__(self, brick_name, brick_config):
        self.brick_name = brick_name
        self.brick_config = brick_config
        self.result = None
        self.proto = None

    def execute(self, *args, force_rerun=False, **kwargs):
        if force_rerun or self.result is None:
            self.proto = kwargs.get("proto", self.proto)
            if self.proto:
                self.result = self._execute(*args, **kwargs)
            else:
                raise Exception("Proto cannot be none")
        return self.result

    @abc.abstractmethod
    def _execute(self, *args, **kwargs):
        pass


class TestBrickRunner(BaseBrickRunner):

    def _execute(self, *args, force_rerun=False, **kwargs):
        return "{}({}_{})".format(self.brick_name, randint(0, 100), self.proto)
