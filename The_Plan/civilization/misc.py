import math
import json

def calculate_distance(loc1, loc2):
    """
    Calculate the Euclidean distance between two points.

    Parameters:
    - loc1 (tuple): First location as (x, y).
    - loc2 (tuple): Second location as (x, y).

    Returns:
    - float: Euclidean distance between the two points.
    """
    return math.sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)

def save_generated_artifact(generated_text, filename="artifact.jsonl"):
    """
    Saves a generated artifact in JSONL format to a file.

    Parameters:
    - generated_text (str): The generated artifact text in string format (JSON).
    - filename (str): The filename to save the artifact. Defaults to 'artifact.jsonl'.
    """
    try:
        artifact_data = json.loads(generated_text)

        with open(filename, 'a') as file:
            json.dump(artifact_data, file)
            file.write("\n")

        # print(f"Artifact saved successfully to {filename}")

    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_to_serializable(obj):
            """Convert non-serializable objects to JSON-compatible types."""
            if isinstance(obj, (np.float32, np.float64, float)):
                return float(obj)
            elif isinstance(obj, (np.int32, np.int64, int)):
                return int(obj)
            elif isinstance(obj, (np.ndarray, list)):
                return obj.tolist()
            return obj