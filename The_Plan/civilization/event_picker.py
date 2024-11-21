import random
import events

def select_random_event(event_type_key):
    """
    Selects a random event from the given event type key.

    Parameters:
    event_type_key (str): The key for the event type in the events dictionary.

    Returns:
    dict: A dictionary containing the event type, outcome, and name.
    """
    event_type = events.Events[event_type_key]
    event_outcome = random.choice(["Positive", "Negative"])
    event_name = random.choice(event_type[event_outcome])

    return {"EventType": event_type_key, "Outcome": event_outcome, "Event": event_name}

def select_event():
    """
    Selects a random event from all event types excluding "Inter-Civilization Interaction".
    """
    event_type_keys = [key for key in events.Events.keys() if key != "Inter-Civilization Interaction"]
    return select_random_event(random.choice(event_type_keys))

def select_neighbor_event():
    """
    Selects a random event from the "Inter-Civilization Interaction" event type.
    """
    return select_random_event("Inter-Civilization Interaction")