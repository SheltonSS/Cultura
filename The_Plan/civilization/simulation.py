from civilization import Civilization
from charts import ArtifactCharts
import analysis

def print_intro():
    """Print the introduction banner for the simulation."""
    print("*************************************************************************\n")
    print("************ Welcome To The Civilization Simulation: Cultura ************\n")
    print("*************************************************************************\n")

def analyze_artifacts():
    """Analyze the generated artifacts and return the average cumulative score."""
    print("Analyzing artifacts...")
    analyzer = analysis.ArtifactAnalyzer(Civilization_Class=Civilization)
    average_score = analyzer.analyze_artifacts()
    print("Average cumulative score of all civilizations' generated artifacts:", average_score)
    return average_score

def create_charts():
    """Generate and save all charts based on the artifacts."""
    charts = ArtifactCharts()
    charts.generate_all_charts()

def generate_civilizations(civs=2):
    """Generate a specified number of civilizations."""
    for i in range(civs):
        civ = Civilization()
        print(f"Generated civilization #{i + 1}: {civ.name} at {civ.location}")

def progress_simulation(steps=2):
    """Run the simulation for a specified number of steps."""
    print("Progressing civilizations...")
    Civilization.progress_and_interact_all_civilizations(steps=steps)

def start_simulation(civs=2, dev_mode=False, steps=2):
    """Run the full simulation."""
    print_intro()
    
    # Set development mode parameters
    if dev_mode:
        Civilization.default_R = int(min(Civilization.map.width, Civilization.map.height) * 1)
        print("Using development mode with R for all civs being:", Civilization.default_R)

    # Generate civilizations
    generate_civilizations(civs=civs)

    # Run the simulation
    progress_simulation(steps=steps)

    # Analyze and create charts
    analyze_artifacts()
    create_charts()

if __name__ == "__main__":
    # Start the simulation with desired parameters
    start_simulation(civs=2, dev_mode=True, steps=2)
