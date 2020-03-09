from .base_brick_processor import BaseBrickProcessor
from ..observer import Publisher
from ..observer.events import EventTypes, OnInputEvent


class InputBrickProcessor(BaseBrickProcessor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process(self, *args, inputs, **kwargs):
        message = OnInputEvent(inputs)
        Publisher().publish_for(event=EventTypes.ON_INPUT_EVENT, message=message)
