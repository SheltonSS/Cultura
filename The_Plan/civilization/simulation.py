import misc
import config
from civilization import Civilization
import random
import json
# Example Integration
if __name__ == "__main__":
    # Randomly assign civilization locations and traits
    # Civilizations 
    location = (1, 1)
    civ1 = Civilization(
        name="Gendaria",
        location=location,
        terrain_type=config.terrain_map[location[0]][location[1]],
        tech_level=random.randint(0, len(config.Tech_eras) - 1)
    )
    location2 = (2, 2)
    civ2 = Civilization(
        name="Mordor",
        location=location2,
        terrain_type=config.terrain_map[location2[0]][location2[1]],
        tech_level=random.randint(0, len(config.Tech_eras) - 1)
    )

    # Print civilizations
    for civ in Civilization.Civilizations:
        print(f"Description: {civ.cultural_context}")
        print(f"Traits of {civ.name}: {civ.traits}")
        print()

    # interact with civilizations
    for civ in Civilization.Civilizations:
        print(f"{civ.name}'s interactions:") 
        civ.interact_with_neighbors()
        
        # print("================\n")
    # civ1.interact_with_neighbors()

    # civ1.progress_age()
    # print("\n================\n")
    # Generate cultural artifacts
    artifacts = civ1.generate_cultural_artifacts(generation_type=1)
    # print(f"\nCultural Artifacts: {artifacts}")
    print(f"\n: {artifacts}")
    
    misc.save_generated_artifact(artifacts)


    # formatted_artifact = {
    #     "name": artifacts.get("Name", ""),
    #     "purpose": artifacts.get("Purpose", ""),
    #     "description": artifacts.get("Description", ""),
    #     "significance": artifacts.get("Significance", "")
    # }

    # civ1.artifacts["Cultural Artifacts"].append(artifacts)
    # print (civ1.artifacts["Cultural Artifacts"]) 


    # Add the artifact to the civilization's artifact list
    # self.artifacts["Cultural Artifacts"].append(artifact)