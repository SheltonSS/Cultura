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
    Saves a generated artifact in the required format for NLPScholar to a file.
    
    Parameters:
    - generated_text (str): The generated artifact text in string format.
    - filename (str): The file name to save the artifact. Defaults to 'artifact.jsonl'.
    """
    # Format the generated text into the required structure
    artifact_data = {"text": generated_text}

    try:
        # Open the file in append mode to save new artifacts without overwriting
        with open(filename, 'a') as file:
            # Dump the artifact data in JSONL format
            json.dump(artifact_data, file)
            file.write("\n")
        
        print(f"Artifact saved successfully to {filename}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
