import random
from dotenv import load_dotenv
import os
import openai
import config
import event_picker
import misc
import map_generation
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key is not set. Check the '.env' file or the 'OPENAI_API_KEY' variable. Stupid.")

class Civilization:
    map = map_generation.TerrainMap()
    Civilizations = []
    Civilizations_by_name = {}
    Default_R = int(min(map.width, map.height) * 1)  # Default range
    Default_Turns = 10
    max_tech_level = len(config.Tech_eras)
    progress_point_limit = 5
    current_year = -4000
    year_progression = 50
    existing_artifacts = []

    @staticmethod
    def get_string_year():
        """Return the current year in human-readable format."""
        return f"{abs(Civilization.current_year)} {'BC' if Civilization.current_year < 0 else 'AD'}"
    
    @staticmethod
    def get_unused_civ_name():
        """
        Selects a random unused civilization name from config.civ_names.
        Ensures the name has not been used by another civilization.
        """
        unused_names = list(set(config.civ_names) - set(Civilization.Civilizations_by_name.keys()))
        if unused_names:
            return random.choice(unused_names)
        else:
            raise ValueError("No unused civilization names available.") 

    @staticmethod
    def place_civilization(civ, x=None, y=None):
        """
        Places a civilization on the map at the given coordinates (x, y).
        If no coordinates are provided, it will place the civilization at a random unoccupied spot.
        Ensures that the spot is available (i.e., not occupied by another civilization).
        """
        print(f"Placing {civ.name}")
        if x is None or y is None:
            # Try to get a random unoccupied location
            location = Civilization.get_random_unoccupied_location()
            if location is None:
                print(f"Could not find a valid location for {civ.name}.")
                return None  # or raise an exception, or retry based on your use case
            x, y = location
        print(f"Attempting to place {civ.name} at x: {x}, y: {y}")

        # Check if the spot is available by ensuring no other civilization is placed at this spot
        if not any(civ.location == (x, y) for civ in Civilization.Civilizations): 
            civ.location = (x, y)  # Set civilization's location
            Civilization.map.civ_map[x][y] = civ  # Assign the civilization to this terrain spot
            print(f"{civ.name} has been placed at ({x}, {y})")
        else:
            print(f"Unable to place {civ.name} at ({x}, {y}), spot is already occupied.")
            return Civilization.place_civilization(civ)  # Retry placement if occupied

        return (x, y)

    @staticmethod
    def get_random_unoccupied_location():
        """Finds and returns a random unoccupied location on the map."""
        terrain_map = Civilization.map.get_terrain_map()  # Correct way to access the terrain map
        width = len(terrain_map)
        height = len(terrain_map[0]) if width > 0 else 0
        print(f"width: {width}, height: {height}")
        
        max_attempts = 100  # Safeguard to prevent infinite loop
        attempts = 0
        
        while attempts < max_attempts:
            # Randomly select coordinates
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            print(f"Trying x: {x}, y: {y} as an unoccupied location")
            
            # Check if the spot is available (no civilization should occupy this spot)
            if not any(civ.location == (x, y) for civ in Civilization.Civilizations):
                print(f"Found unoccupied location at x: {x}, y: {y}")
                return x, y
            
            attempts += 1
        
        # If we reach here, no unoccupied spot was found
        print("Max attempts reached without finding an unoccupied location.")
        return None  # Or you could raise an exception here if desired

    def __init__(self, name=None, location=None, tech_level=0):
        """
        Initialize a civilization with traits and a location.
        
        Parameters:
        - name: Name of the civilization
        - location: (x, y) tuple on the map
        - tech_level: Technological advancement level (1-9)
        """
        # Assign name if not provided
        self.name = name or Civilization.get_unused_civ_name()
        print(f"New civilization: {self.name}")

        # Assign location if not provided
        self.location = location or Civilization.place_civilization(self)
        print(f"{self.name} has been placed at {self.location}")

        # Set terrain type based on the location
        self.terrain_type = Civilization.map.get_terrain_map()[self.location[0]][self.location[1]]

        # Set tech level and traits
        self.tech_level = tech_level
        self.traits = self.assign_traits()

        # Generate cultural context and history
        self.cultural_context = self.generate_cultural_context()
        self.artifacts = {"Historical artifacts": [], "Interaction artifacts": []}
        self.history = [f"Founded {self.name} in a {self.get_terrain_description()} region during the {config.Tech_eras[self.tech_level]} era."]
        self.neighbors = []
        self.neighbor_history = []

        # Update civilization-wide properties
        Civilization.year_progression = Civilization.calculate_year_progression()
        Civilization.Civilizations.append(self)
        Civilization.Civilizations_by_name[self.name] = self

        # Find neighbors
        for civ in Civilization.Civilizations:
            civ.find_neighbors()

    def assign_traits(self):
        """Assign traits based on terrain type and random factors."""
        random_trait = random.choice(["Innovative", "Tradition-Oriented", "Expansive", "Artistic"])
        return config.base_traits.get(self.terrain_type, ["Undefined"]) + [random_trait]
    

    def expand_territory(self):
        """Expand the civilization's territory to nearby tiles."""
        x, y = self.location
        expansion_radius = 2
        for dx in range(-expansion_radius, expansion_radius + 1):
            for dy in range(-expansion_radius, expansion_radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < Civilization.map.width and 0 <= ny < Civilization.map.height:
                    if Civilization.map.get_terrain_map()[nx][ny] is None:
                        Civilization.map.get_terrain_map()[nx][ny] = self
                        print(f"{self.name} has expanded to ({nx}, {ny})")

    def find_neighbors(self):
        """Find and add civilizations within a given radius to the neighbors list."""
        self.neighbors = []
        for civ in Civilization.Civilizations:
            if civ != self:
                # distance = misc.calculate_distance(self.location, civ.location)
                # if distance <= Civilization.Default_R:
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

    def generate_cultural_artifacts(self, model="gpt-3.5-turbo", max_tokens=350, temperature=0.7, generation_type="history"):
        """Generate a unique cultural artifact description using ChatGPT."""
        # regular generation mode
        prompt = f""" 
        Describe a unique cultural artifact of type '{random.choice(config.artifact_types)}' made during the {config.Tech_eras[self.tech_level]} era, including its purpose, using the following cultural context:

        Civilization Name: {self.name}
        Region: {self.get_terrain_description()}
        Traits: {', '.join(self.traits)}
        Tech Level: {config.Tech_eras[self.tech_level]}
        Current Time Period: {Civilization.get_string_year()} - {abs(Civilization.current_year + Civilization.year_progression)}{'BC' if Civilization.current_year + Civilization.year_progression < 0 else 'AD'}

        The response should be in the following JSON format:

            {config.json_format}

        Be sure to integrate aspects of the civilization into the artifact, selecting aspects of their values, environment, and technological level to shape the artifact's form and function.

        """

        if generation_type == "history":  # history generation mode
            prompt += f"\nThe response should also consider the civilization's history: {', '.join(self.history)}"
        if generation_type == "neighbor":  # neighbor generation mode
            if len(self.neighbors) == 0:
                raise ValueError("No neighbors found for this civilization.")
            prompt += "\nThe response should also consider the civilization's interactions with neighboring civilizations:"
            # prompt += f"\nNeighboring Civilizations:\n {[neighbor.cultural_context for neighbor in self.neighbors]}"
            
            prompt += f"\nNeighboring Civilizations Interaction History:\n {', '.join(self.neighbor_history)}"

        # print (prompt)
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )

            year_made_I = random.randint(Civilization.current_year, Civilization.current_year + Civilization.year_progression)
            artifact_data = json.loads(response['choices'][0]['message']['content'])
            artifact_data["generation_type"] = generation_type
            artifact_data["Year Made"] = f"{abs(year_made_I)} {'BC' if year_made_I  < 0 else 'AD'}"
            artifact_data["Civilization Name"] = self.name
            artifact_description = json.dumps(artifact_data, indent=2)

            if generation_type == "history":
                self.artifacts["Historical artifacts"].append(artifact_description)
            elif generation_type == "neighbor":
                self.artifacts["Interaction artifacts"].append(artifact_description)
            else:
                print(f"Unknown generation type: {generation_type}")

            Civilization.existing_artifacts.append(artifact_description)
            print (f"\nArtifact: {artifact_description}")
            return artifact_description

        except openai.error.OpenAIError as e:
            return f"OpenAI API error: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"

        
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

    def interact_with_neighbors(self, neighbor_interaction_limit = 5):
        """Interact with neighbors, adding or removing traits based on the interaction type."""
        
        cultural_crossing_limit = max(2, neighbor_interaction_limit // 2)

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
                # print(f"Generated Historical Artifact: {artifact}")
            
                misc.save_generated_artifact(artifact)
                civilization.interact_with_neighbors()
                artifact = civilization.generate_cultural_artifacts(generation_type = "neighbor")
                # print(f"Generated Interaction Artifact: {artifact}")
                misc.save_generated_artifact(artifact)

            Civilization.current_year += Civilization.year_progression
            Civilization.year_progression = Civilization.calculate_year_progression()
