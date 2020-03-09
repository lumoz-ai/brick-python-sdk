from .base_brick_processor import BaseBrickProcessor


class InputBrickProcessor(BaseBrickProcessor):

    def __init__(self, *args, brick, **kwargs):
        super().__init__(*args, **kwargs)
        self.brick = brick

    def process(self, *args, inputs, **kwargs):
        return self.brick.execute(inputs=inputs)
