import random
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from dotenv import load_dotenv
import os
import openai
import config
# from events.event_pseicker import select_event
from event_picker import select_event  # Import the dictionary directly

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
        self.artifacts = {"Cultural Artifacts": []}
        self.history = []
        self.history.append(f"Founded { self.name } in a { self.get_terrain_description() } region during the { config.Tech_eras[self.tech_level] } era.")
        self.progress_point_limit = 10

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
        context += f"With a technology level of {config.Tech_eras[self.tech_level]}."
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

    
    def generate_cultural_artifacts(self, model="gpt-4", max_tokens=400, temperature=0.7,gen_type=0):
        """
        Generates a unique cultural artifact description using ChatGPT.
        """
        # prompt ==============================================================
        prompt = f"""
        Describe a unique cultural artifact of type '{random.choice(config.artifact_types)}' made during the {config.Tech_eras[self.tech_level]} era, including its purpose and significance, using the following cultural context:

        Civilization Name: {self.name}
        Region: {self.terrain_type}
        Traits: {', '.join(self.traits)}

        The civilization is known for those qualities, which should influence the cultural artifact generated. Consider how these traits, the environment, and the technology level might impact the design, purpose, and significance of the artifact.

        Here are the general definitions for the technological eras:

            {config.Tech_eras_string}

        The response should be in the following json format:

            {config.json_format}

        Be sure to integrate and weve aspects of the civilization into the artifact, select aspecsts of their values, environment, and technological level should shape the artifact's form and function.
        """

        if gen_type == 1:
            prompt += f"""\n

            The response should also take into consideration the following history of the civilization:

            {', '.join(self.history)}

            """

        #query Model =======================================================
        try:
            # query the model
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            
            # return the artifact description
            self.artifacts["Cultural Artifacts"].append(response['choices'][0]['message']['content'])
            return response['choices'][0]['message']['content']
        
        except Exception as e:
            return f"Error generating artifact: {e}"
        
    def progress_era(self):
        """
        Progress the civilization to the next technological era. This increases tech level,
        may add or remove traits, and updates the cultural context.
        """
        # Increase tech level
        if self.tech_level < 9:
            self.tech_level += 1
            print(f"{self.name} has progressed to the {config.Tech_eras[self.tech_level]} era.")
            self.history.append(f"{self.name} has progressed to the {config.Tech_eras[self.tech_level]} era.")


        # Add or remove traits
        if random.random() > 0.5:  # 50% chance to gain a new trait
            new_trait = random.choice(["Visionary", "Pragmatic", "Ambitious", "Altruistic"])
            if new_trait not in self.traits:
                self.traits.append(new_trait)
                self.history.append(f"{self.name} has gained a new trait: {new_trait}")
                print(f"{self.name} has gained a new trait: {new_trait}")

        if len(self.traits) > 3 and random.random() > 0.7:  # 30% chance to lose a random trait
            removed_trait = random.choice(self.traits)
            self.traits.remove(removed_trait)
            self.history.append(f"{self.name} has lost a trait: {removed_trait}")
            print(f"{self.name} has lost a trait: {removed_trait}")

        # Update cultural context
        self.cultural_context = self.generate_cultural_context()

    def regress_era(self):
        """
        Regress the civilization to a previous technological era. This decreases the tech level
        and may remove traits, reflecting a decline in progress.
        """
        # Decrease tech level
        if self.tech_level > 1:
            self.tech_level -= 1
            print(f"{self.name} has regressed back to the {config.Tech_eras[self.tech_level]} era.")
            self.history.append(f"{self.name} has regressed back to the {config.Tech_eras[self.tech_level]} era.")


        # Remove traits with some probability
        if len(self.traits) > 3 and random.random() > 0.5:  # 50% chance to lose a trait
            removed_trait = random.choice(self.traits)
            self.traits.remove(removed_trait)
            self.history.append(f"{self.name} has lost a trait: {removed_trait}")
            print(f"{self.name} has lost a trait: {removed_trait}")

        # Update cultural context
        self.cultural_context = self.generate_cultural_context()

    def progress_age(self):
        pp = 0
        while self.tech_level < 9 and pp < self.progress_point_limit:
            selected_event = select_event()
            pos = 0
            neg = 0
            if selected_event["Outcome"] == "positive":
                pos += 1
            else:
                neg += 1
            pp+=1
            self.history.append(f"{selected_event['Outcome']} {selected_event['EventType']}: {selected_event['Event']}")
        
        if pos > neg:
            self.progress_era()
        elif pos < neg:
            self.regress_era()

        print("\n================\n")
        for i in self.history:
            print(i)
        # print(self.history)

                
# Example Integration
if __name__ == "__main__":
    # Randomly assign civilization locations and traits
    location = (1, 1)
    civ1 = Civilization(
        name="Gendaria",
        location=location,
        terrain_type=config.terrain_map[location[0]][location[1]],
        tech_level=random.randint(1, 5)
    )
    print(f"Description: {civ1.cultural_context}")
    print()
    print(f"Traits of {civ1.name}: {civ1.traits}")

    civ1.progress_age()
    print("\n================\n")
    # Generate cultural artifacts
    artifacts = civ1.generate_cultural_artifacts(gen_type=1)
    print(f"\nCultural Artifacts: {artifacts}")
    # print(select_event())
    # Progress the civilization
    # for i in range(3):
    #     civ1.progress_era()
        # print(f"\nProgressed Civilization:\n{civ1.cultural_context}")
        # print("\n================")

    # Regress an era
    # civ1.regress_era()
    # print(f"\nRegressed Civilization:\n{civ1.cultural_context}")
    # print("\n================\n")


