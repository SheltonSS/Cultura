import random
from dotenv import load_dotenv
import os
import openai
import config
import event_picker
import misc
import map_generation

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key is not set. Check the '.env' file or the 'OPENAI_API_KEY' variable. Stupid.")

class Civilization:
    Civilizations = []
    Default_R = 5
    Default_Turns = 10
    max_tech_level = len(config.Tech_eras)
    progress_point_limit = 5
    current_year = -4000
    year_progression = 50
    # print("class map generation")
    map = map_generation.TerrainMap()

    @staticmethod
    def get_string_year():
        """Return the current year in human-readable format."""
        return f"{abs(Civilization.current_year)} {'BC' if Civilization.current_year < 0 else 'AD'}"

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
        self.neighbors = []
        self.neighbor_history = []

        # Update civilization-wide properties
        Civilization.Default_R = int(min(Civilization.map.width, Civilization.map.height) * 0.1)
        Civilization.year_progression = Civilization.calculate_year_progression()
        Civilization.Civilizations.append(self)

        # Find neighbors
        for civ in Civilization.Civilizations:
            civ.find_neighbors(Civilization.Default_R)

    def assign_traits(self):
        """Assign traits based on terrain type and random factors."""
        random_trait = random.choice(["Innovative", "Tradition-Oriented", "Expansive", "Artistic"])
        return config.base_traits.get(self.terrain_type, ["Undefined"]) + [random_trait]
    
    def find_neighbors(self, radius):
        """
        Find and add civilizations within a given radius to the neighbors list.

        Parameters:
        - radius (float): The distance within which other civilizations are considered neighbors.
        """
        self.neighbors = []
        for civ in Civilization.Civilizations:
            if civ != self:
                distance = misc.calculate_distance(self.location, civ.location)
                if distance <= radius:
                    self.neighbors.append(civ)

    def blend_cultures(self, artifact_traits):
        for neighbor in self.neighbors:
            if neighbor["interaction_type"] == "Trade":
                # Positive blending of traits
                artifact_traits.append(random.choice(neighbor["traits"]))
            elif neighbor["interaction_type"] == "Conflict":
                # Resistance or reactive blending
                artifact_traits.append(f"Anti-{random.choice(neighbor['traits'])}")
        return artifact_traits

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

    def generate_cultural_artifacts(self, model="gpt-3.5-turbo", max_tokens=350, temperature=0.7, generation_type=1):
        """Generate a unique cultural artifact description using ChatGPT."""
        # regular generation mode
        prompt = f""" 
        Describe a unique cultural artifact of type '{random.choice(config.artifact_types)}' made during the {config.Tech_eras[self.tech_level]} era, including its purpose and significance, using the following cultural context:

        Civilization Name: {self.name}
        Region: {self.get_terrain_description()}
        Traits: {', '.join(self.traits)}

        Here are the general definitions for the technological eras:

        {config.Tech_eras_string}

        The response should be in the following JSON format:

            {config.json_format}

        Be sure to integrate aspects of the civilization into the artifact, selecting aspects of their values, environment, and technological level to shape the artifact's form and function.

        Current Time Period: {Civilization.get_string_year()} - {abs(Civilization.current_year + Civilization.year_progression)}{'BC' if Civilization.current_year + Civilization.year_progression < 0 else 'AD'}
        """

        if generation_type == 1:  # history generation mode
            prompt += f"The response should also consider the civilization's history: {', '.join(self.history)}"
        if generation_type == 2:  # neighbor generation mode
            prompt += f"Neighboring Civilizations: {[neighbor.cultural_context for neighbor in self.neighbors]}"
            
            prompt += f"Neighboring Civilizations Interaction History: {', '.join(self.neighbor_history)}"

        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )

            artifact_description = response['choices'][0]['message']['content']
            # print("\ndescription", artifact_description)
            year_made_I = random.randint(Civilization.current_year, Civilization.current_year + Civilization.year_progression)
            year_made = f'"Year Made": "{abs(year_made_I)} {"BC" if year_made_I < 0 else "AD"}"'
            year_made+= "}"
            # print(f"\n{artifact_description[:artifact_description.find('}')]},\n{year_made}")
            artifact_description = f"{artifact_description[:artifact_description.find('}')]},\n{year_made}"
            self.artifacts["Cultural Artifacts"].append(artifact_description)

            return artifact_description

        except Exception as error:
            return f"Error generating artifact: {error}"
        
    def progress_era(self):
        """Progress the civilization to the next technological era."""
        if self.tech_level < Civilization.max_tech_level - 1:
            self.tech_level += 1
            self.history.append(f"{self.name} has progressed to the {config.Tech_eras[self.tech_level]} era.")

        # Add or remove traits
        if random.random() > 0.5:  # 50% chance to gain a new trait
            new_trait = random.choice(["Visionary", "Pragmatic", "Ambitious", "Altruistic"])
            if new_trait not in self.traits:
                self.traits.append(new_trait)
                self.history.append(f"{self.name} has gained a new trait: {new_trait}")
                # print(f"{self.name} has gained a new trait: {new_trait}")

        if len(self.traits) > 3 and random.random() > 0.7:  # 30% chance to lose a random trait
            removed_trait = random.choice(self.traits)
            self.traits.remove(removed_trait)
            self.history.append(f"{self.name} has lost a trait: {removed_trait}")
            # print(f"{self.name} has lost a trait: {removed_trait}")

        # Update cultural context
        self.cultural_context = self.generate_cultural_context()

    def regress_era(self):
        """Regress the civilization to the previous technological era."""
        if self.tech_level > 1:
            self.tech_level -= 1
            # print(f"{self.name} has regressed back to the {config.Tech_eras[self.tech_level]} era.")
            self.history.append(f"{self.name} has regressed back to the {config.Tech_eras[self.tech_level]} era.")

        # Remove traits with some probability
        if len(self.traits) > 3 and random.random() > 0.5:  # 50% chance to lose a trait
            removed_trait = random.choice(self.traits)
            self.traits.remove(removed_trait)
            self.history.append(f"{self.name} has lost a trait: {removed_trait}")
            # print(f"{self.name} has lost a trait: {removed_trait}")

        # Update cultural context
        self.cultural_context = self.generate_cultural_context()

    def progress_age(self):
        """Progress the civilization through an age."""
        # Civilization.current_year += Civilization.year_progression
        progress_points = 0
        positive_outcomes = 0
        negative_outcomes = 0

        while progress_points < Civilization.progress_point_limit:
            event = event_picker.select_event()
            progress_points += 1
            if event["Outcome"] == "Positive":
                positive_outcomes += 1
            else:
                negative_outcomes += 1
            self.history.append(f"{event['Outcome']} {event['EventType']}: {event['Event']}")

        if positive_outcomes > negative_outcomes:
            self.progress_era()
        elif negative_outcomes > positive_outcomes:
            self.regress_era()

        print(f"\n ================================\n History for {self.name}: {Civilization.get_string_year()} - {abs(Civilization.current_year + Civilization.year_progression)} \n================================\n")
        for history_entry in self.history:
            print(history_entry)

        Civilization.year_progression = Civilization.calculate_year_progression()

    def interact_with_neighbors(self):
        """Interact with neighbors, adding or removing traits based on the interaction type."""
        neighbor_interaction_limit = 5
        cultural_crossing_limit = neighbor_interaction_limit // 2

        positive_interactions = 0
        negative_interactions = 0
        criss_cross = ""

        for _ in range(neighbor_interaction_limit):
            event = event_picker.select_neighbor_event()

            for neighbor in self.neighbors:
                if event["Outcome"] == "Positive":
                    positive_interactions += 1
                    # Check if positive interactions exceed the threshold for cultural exchange
                    if positive_interactions > cultural_crossing_limit:
                        # Cross-cultural exchange
                        self_trait = random.choice(self.traits) 
                        neighbor_trait = random.choice(neighbor.traits)

                        self.traits.append(neighbor_trait)  
                        neighbor.traits.append(self_trait)

                        positive_interactions -= negative_interactions
                        negative_interactions = negative_interactions // 2
                        
                        criss_cross = f"Repeated positive exposure has resulted in a cultural exchange between {self.name} and {neighbor.name}.\n{self.name} received the {neighbor_trait} trait from {neighbor.name} and {neighbor.name} received the {self_trait} trait from {self.name}."
                else:
                    negative_interactions += 1

                # Record the interaction in the history for both civilizations
                self.neighbor_history.append(f"{self.name} interacted with {neighbor.name} {event['Outcome']}ly: {event['Event']}")
                neighbor.neighbor_history.append(f"{self.name} interacted with {neighbor.name} {event['Outcome']}ly: {event['Event']}")

                if criss_cross:
                    self.neighbor_history.append(criss_cross)
                    neighbor.neighbor_history.append(criss_cross)
                    criss_cross = ""
        # Print the neighbor history for this civilization
        print("\n================\n")
        for history_entry in self.neighbor_history:
            print(history_entry)


    @staticmethod
    def calculate_year_progression():
        """Calculate year progression based on the average tech level."""
        if not Civilization.Civilizations:
            return 100
        avg_tech_level = sum(civ.tech_level for civ in Civilization.Civilizations) / len(Civilization.Civilizations)
        return max(1, int(50 / (avg_tech_level / Civilization.max_tech_level + 0.5)))

    @staticmethod
    def progress_and_interact_all_civilizations(steps=5):
        """Run the simulation for all civilizations for a number of steps."""
        for step in range(steps):
            for civilization in Civilization.Civilizations:
                civilization.progress_age()
                artifact = civilization.generate_cultural_artifacts()
                print(f"Generated Historical Artifact: {artifact}")
                misc.save_generated_artifact(artifact)
                civilization.interact_with_neighbors()
                artifact = civilization.generate_cultural_artifacts(generation_type=2)
                print(f"Generated Interaction Artifact: {artifact}")
                misc.save_generated_artifact(artifact)

            Civilization.current_year += Civilization.year_progression
            Civilization.year_progression = Civilization.calculate_year_progression()
