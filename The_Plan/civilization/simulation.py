import misc
import config
from civilization import Civilization
import map_generation
import random
import json

if __name__ == "__main__":
    # Randomly assign civilization locations and traits
    # Civilizations 
    # This is a workshop to test the simulation
    map = Civilization.map
    Civilization.default_R = int(min(Civilization.map.width, Civilization.map.height) * 1)

    location = (random.randint(0, len(Civilization.map.get_terrain_map()) - 1), random.randint(0, len(Civilization.map.get_terrain_map()[0]) - 1))
    civ1 = Civilization(
        name="Shelleian",
        location=location,
        terrain_type=Civilization.map.get_terrain_map()[location[0]][location[1]],
        # tech_level=random.randint(0, len(config.Tech_eras) - 1)
        tech_level=0
    )

    location2 = (random.randint(0, len(Civilization.map.get_terrain_map()) - 1), random.randint(0, len(Civilization.map.get_terrain_map()[0]) - 1))
    while location2 == location:
            location2 = (random.randint(0, len(Civilization.map.get_terrain_map()) - 1), random.randint(0, len(Civilization.map.get_terrain_map()[0]) - 1))


    civ2 = Civilization(
        name="Novile",
        location=location2,
        terrain_type=Civilization.map.get_terrain_map()[location2[0]][location2[1]],
        # tech_level=random.randint(0, len(config.Tech_eras) - 1)
        tech_level=0
    )

    Civilization.progress_and_interact_all_civilizations(steps=10)    

    for civ in Civilization.Civilizations:
        print()
        print(f"Name: {civ.name}")
        print(f"Description: {civ.cultural_context}")
        print(f"Traits of {civ.name}: {civ.traits}")
        print()
        print(f"History: {civ.history}")
        print()
        print(f"Interactions: {civ.neighbor_history}")


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