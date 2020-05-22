import _thread

from ..utils import Singleton


class Publisher(metaclass=Singleton):
    def __init__(self, default_event_channel="default_channel"):
        self._default_event_channel = default_event_channel
        self.subscribers = {self._default_event_channel: dict()}

    def register_subscriber_for(self, event, subscriber, callback_method=None):
        if callback_method is None:
            callback_method = getattr(subscriber, "update")
        if self.get_subscribers_for(event) is None:
            self.subscribers[event] = dict()
        self.subscribers[event][subscriber] = callback_method

    def unregister_subscriber_for(self, event, subscriber):
        del self.get_subscribers_for(event)[subscriber]

    def publish_for(self, event, message):
        _thread.start_new_thread(self._publish_for, (event, message))

    def _publish_for(self, event, message):
        subscribers = self.get_subscribers_for(event)
        if subscribers is not None:
            for subscriber, callback_method in subscribers.items():
                callback_method(message)
        else:
            print("No subscribers for that event")

    def get_subscribers_for(self, event):
        return self.subscribers.get(event, None)
