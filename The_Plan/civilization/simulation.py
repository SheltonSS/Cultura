from civilization import Civilization
import analysis

if __name__ == "__main__":
    # Randomly assign civilization locations and traits
    # Civilizations 
    # This is a workshop to test the simulation

    print("Starting simulation...")
    print("Map created")
    print(f"Map width: {Civilization.map.width}, Map height: {Civilization.map.height}")
    Civilization.default_R = int(min(Civilization.map.width, Civilization.map.height) * 1)  # Test range set to the whole map
    print("using development test range")

    # generate civ1
    civ1 = Civilization()
    print("made civ1")

    # generate civ2
    civ2 = Civilization()
    print("made civ2")

    print("generated civilizations:")
    for civ in Civilization.Civilizations:
        print(f"{civ.name} at {civ.location}")

    print("progressing civilizations...")
    Civilization.progress_and_interact_all_civilizations(steps=1)    

    # analyze artifacts
    print("analyzing artifacts...")
    analyzer = analysis.ArtifactAnalyzer(Civilization_Class=Civilization)
    # artifacts = analyzer.load_artifacts()
    print("\Average cumulative score of all civilization's generated artifacts:", analyzer.analyze_artifacts())
    