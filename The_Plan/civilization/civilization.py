import random
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key is not set. Check the '.env' file or the 'OPENAI_API_KEY' variable. Stupid.")


class Civilization:
    def __init__(self, name, location, terrain_type, tech_level):
        """
        Initialize a civilization with traits and a location.
        
        Parameters:
        - name: Name of the civilization
        - location: (x, y) tuple on the map
        - terrain_type: The terrain type from the map (water, plains, etc.)
        - tech_level: Technological advancement level (1-9)
        """
        self.name = name
        self.location = location
        self.terrain_type = terrain_type
        self.tech_level = tech_level
        self.traits = self.assign_traits()
        self.cultural_context = self.generate_cultural_context()

    def assign_traits(self):
        """Assign traits based on terrain type and random factors."""
        base_traits = {
            0: ["Maritime", "Resourceful", "Nomadic"],  # Water
            1: ["Agrarian", "Peaceful", "Communal"],    # Plains
            2: ["Hardy", "Independent", "Resilient"],   # Hills
            3: ["Isolationist", "Strategic", "Defensive"],  # Mountains
            5: ["Adaptive", "Spiritual", "Tough"],      # Tundra
        }

        random_trait = random.choice(["Innovative", "Tradition-Oriented", "Expansive", "Artistic"])
        return base_traits.get(self.terrain_type, ["Undefined"]) + [random_trait]

    def generate_cultural_context(self):
        """Create a description of the civilization's culture based on traits and tech level."""
        context = f"{self.name} is a civilization located in a {self.get_terrain_description()} region. "
        context += f"They are known for being {' and '.join(self.traits[:-1])}, with a particularly {self.traits[-1]} nature. "
        context += f"With a technology level of {self.tech_level}/9."
        return context

    def get_terrain_description(self):
        """Return a human-readable description of the terrain type."""
        descriptions = {
            0: "maritime",
            1: "fertile plains",
            2: "rolling hills",
            3: "rugged mountains",
            5: "harsh tundra",
        }
        return descriptions.get(self.terrain_type, "unknown terrain")

    
    def generate_cultural_artifacts(self, model="gpt-4", max_tokens=200, temperature=0.7):
        """
        Generates a unique cultural artifact description using ChatGPT.
        """
        prompt = f"""
        Describe a unique cultural artifact, including its purpose and significance using the following cultural context:
        {self.cultural_context}

        The cultural artifact should be a natural.
        Here are thet general definitions for the technological eras:
        1:Ancient
        2:Classical
        3:Medieval
        4:Renaissance
        5:Industrial
        6:Modern
        7:Atomic
        8:Information
        9:Future

        The response should be in the following json format:
            Name
            Creation Date
            Description 
            purpose
            Significance
        """
        
        try:
            # Query the ChatGPT model
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            
            # Extract and return the artifact description
            return response['choices'][0]['message']['content']
        
        except Exception as e:
            return f"Error generating artifact: {e}"

# Example Integration
if __name__ == "__main__":
    # Simulate a terrain map with a few civilization placements
    terrain_map = [
        [1, 1, 0, 3, 5],
        [1, 2, 2, 3, 5],
        [0, 1, 1, 2, 5],
    ]
    
    # Randomly assign civilization locations and traits
    civ1 = Civilization(
        name="Thalrathians",
        location=(1, 1),
        terrain_type=terrain_map[1][1],
        tech_level=random.randint(1, 9)
    )
    
    print(f"Traits of {civ1.name}: {civ1.traits}")
    print()
    print(f"Description: {civ1.cultural_context}")
    print("\n================\n")
    
    # Load tokenizer and model
    # model_name = "meta-llama/Llama-3.2-1B-Instruct"
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    # model = AutoModelForCausalLM.from_pretrained(model_name)

    # Generate cultural artifacts
    artifacts = civ1.generate_cultural_artifacts()
    print(f"\nCultural Artifacts: {artifacts}")
