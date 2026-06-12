class EventBus:

    def __init__(self):

        self.handlers = {}

    def subscribe(self, event_type, handler):

        if event_type not in self.handlers:

            self.handlers[event_type] = []

        self.handlers[event_type].append(handler)

    def publish(self, event):

        event_type = type(event)

        for handler in self.handlers.get(event_type, []):

            handler(event)


event_bus = EventBus()