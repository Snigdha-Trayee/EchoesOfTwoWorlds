
class CinematicEventManager:
    def __init__(self):
        self.triggered_events = set()
        self.pending_events = []

    def trigger(self, event_id, payload=None):
        if event_id in self.triggered_events:
            return False

        self.triggered_events.add(event_id)

        self.pending_events.append({
            "event": event_id,
            "payload": payload or {},
        })

        return True

    def get_next_event(self):
        if not self.pending_events:
            return None

        return self.pending_events.pop(0)

    def has_triggered(self, event_id):
        return event_id in self.triggered_events

    def reset(self):
        self.triggered_events.clear()
        self.pending_events.clear()
