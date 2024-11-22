import misc
import config
from civilization import Civilization
import random
import json

if __name__ == "__main__":
    # Randomly assign civilization locations and traits
    # Civilizations 
    location = (random.randint(0, len(config.terrain_map) - 1), random.randint(0, len(config.terrain_map[0]) - 1))
    civ1 = Civilization(
        name="Borf",
        location=location,
        terrain_type=config.terrain_map[location[0]][location[1]],
        tech_level=random.randint(0, len(config.Tech_eras) - 1)
    )
    
    location2 = location
    while location2 == location:
        location2 = (random.randint(0, len(config.terrain_map) - 1), random.randint(0, len(config.terrain_map[0]) - 1))

    civ2 = Civilization(
        name="Shelley",
        location=location2,
        terrain_type=config.terrain_map[location2[0]][location2[1]],
        tech_level=random.randint(0, len(config.Tech_eras) - 1)
    )

    Civilization.progress_and_interact_all_civilizations()

    # Print civilizations
    # for i in range(10//len(Civilization.Civilizations)):
    # for i in range(1):
    #     for civ in Civilization.Civilizations:
    #         print(f"Description: {civ.cultural_context}")
    #         print(f"Traits of {civ.name}: {civ.traits}")
    #         print()

    # # interact with civilizations
    # for civ in Civilization.Civilizations:
    #     print(f"{civ.name}'s interactions:") 
    #     civ.interact_with_neighbors()
    #     civ.

    # # Generate cultural artifacts from neighbor interactions
    # artifact = civ1.generate_cultural_artifacts(generation_type=2)
    # print(f"\n: {artifact}")
    # misc.save_generated_artifact(artifact)