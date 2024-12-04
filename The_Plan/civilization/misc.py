import math
import json

def calculate_distance(loc1, loc2):
    """Calculate the Euclidean distance between two points on a map."""
    return math.sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)

def save_generated_artifact(generated_text, filename="artifact.jsonl"):
    """Saves a generated artifact in JSONL format to a file."""
    try:
        artifact_data = json.loads(generated_text)

        with open(filename, 'a') as file:
            json.dump(artifact_data, file)
            file.write("\n")

    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")