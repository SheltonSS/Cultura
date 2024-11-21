import random
import events

def select_event():
    # Randomly select an event type and whether it's positive or negative
    event_type = random.choice(list(events.Events.keys()))  # Pick a random event type (e.g., "Technological_Events")
    event_outcome = random.choice(["Positive", "Negative"])  # Pick either "Positive" or "Negative"

    # Get a random event from the selected category and outcome
    event_name = random.choice(events.Events[event_type][event_outcome])

    # Display the results
    # print(f"Event Type: {event_type}")
    # print(f"Outcome: {event_outcome}")
    # print(f"Event: {event_name}")

    return {"EventType": event_type, "Outcome": event_outcome, "Event": event_name}
print (select_event())