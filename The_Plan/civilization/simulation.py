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
    used_names = set()
    used_locations = set()

    map = Civilization.map
    Civilization.default_R = int(min(Civilization.map.width, Civilization.map.height) * 1)  # Test range set to the whole map

    # Generate civ1
    while True:
        name = random.choice(config.civ_names)
        if name not in used_names:
            used_names.add(name)
            break

    while True:
        location = (
            random.randint(0, len(Civilization.map.get_terrain_map()) - 1),
            random.randint(0, len(Civilization.map.get_terrain_map()[0]) - 1),
        )
        if location not in used_locations:
            used_locations.add(location)
            break

    civ1 = Civilization(
        name=name,
        location=location,
    )

    # Generate civ2
    while True:
        name = random.choice(config.civ_names)
        if name not in used_names:
            used_names.add(name)
            break

    while True:
        location2 = (
            random.randint(0, len(Civilization.map.get_terrain_map()) - 1),
            random.randint(0, len(Civilization.map.get_terrain_map()[0]) - 1),
        )
        if location2 not in used_locations:
            used_locations.add(location2)
            break

    civ2 = Civilization(
        name=name,
        location=location2,
    )

    print(f"Civilization 1: {civ1.name} , {civ1.location}")
    print(f"Civilization 2: {civ2.name} , {civ2.location}")

    Civilization.progress_and_interact_all_civilizations(steps=10)    

    # Print civilizations summation
    print("\n===============================\nCivilizations:")
    for civ in Civilization.Civilizations:
        print()
        print(f"Name: {civ.name}")
        print(f"Description: {civ.cultural_context}")
        print(f"Traits of {civ.name}: {civ.traits}")
        print()
        print(f"History: {civ.history}")
        print()
        print(f"Interactions: {civ.neighbor_history}")
        print()
        print(f"Artifacts: {civ.artifacts}")
        print()

        # analyze artifacts
        for artifact in civ.artifacts["Historical artifacts"]:
            print(f"Artifact: {artifact}")


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