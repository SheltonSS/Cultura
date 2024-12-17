import random
import events

def select_event(event_type_key=None, exclude_key="Inter-Civilization Interaction"):
    """
    Selects a random event. If `event_type_key` is specified, selects from that type.
    If not, selects from all event types, optionally excluding a specific key.

    Parameters:
    event_type_key (str, optional): Specific event type to select from.
    exclude_key (str, optional): Event type to exclude when selecting randomly.

    Returns:
    dict: A dictionary containing the event type, outcome, and name.
    """
    if event_type_key is None:
        event_type_keys = [key for key in events.Events if key != exclude_key]
        event_type_key = random.choice(event_type_keys)

    event_type = events.Events[event_type_key]
    return {
        "EventType": event_type_key,
        "Outcome": (outcome := random.choice(["Positive", "Negative"])),
        "Event": random.choice(event_type[outcome]),
    }
