# import pygame
from civilization import Civilization
from charts import ArtifactCharts
import analysis
from map_generation import TerrainMap
import random

class CulturaSimulation:
    def __init__(self, civs=2, dev_mode=False, ages=2, width=25, height=25,speed_multiplier=1):
        self.civs = civs
        self.dev_mode = dev_mode
        self.ages = ages
        self.width = width
        self.height = height
        self.civiliation_class = Civilization
        self.civiliation_class.speed_multiplier = speed_multiplier
        self.civilizations = []
        self.terrain_map = self.civiliation_class.map.get_terrain_map()
        # self.terrain_map = TerrainMap(width=width, height=height, base_scale=40.0, octaves=6)

        # Set up Pygame window
        # self.cell_size = 20
        # self.screen = pygame.display.set_mode((self.width * self.cell_size, self.height * self.cell_size))
        # pygame.display.set_caption("Cultura: Civilization Simulation")

    def print_intro(self):
        """Print the introduction banner for the simulation."""
        print("*************************************************************************\n")
        print("************ Welcome To The Civilization Simulation: Cultura ************\n")
        print("*************************************************************************\n")

    def analyze_artifacts(self):
        """Analyze the generated artifacts and return the average cumulative score."""
        print("Analyzing artifacts...")
        analyzer = analysis.ArtifactAnalyzer(Civilization_Class=Civilization)
        average_score = analyzer.analyze_artifacts()
        print("Average cumulative score of all civilizations' generated artifacts:", average_score)
        return average_score

    def create_charts(self):
        """Generate and save all charts based on the artifacts."""
        charts = ArtifactCharts()
        charts.generate_all_charts()

    def generate_civilizations(self):
        """Generate a specified number of civilizations."""
        for i in range(self.civs):
            Civilization()
            # self.civilizations.append(civ)
            print(f"Generated civilization #{i + 1}: {Civilization.Civilizations[i].name} at {Civilization.Civilizations[i].location}")

    def progress_simulation(self):
        """Run the simulation for a specified number of ages."""
        print("Progressing civilizations...")
        Civilization.progress_and_interact_all_civilizations(ages=self.ages)

    # def visualize_terrain(self):
    #     """Visualize the terrain map."""
    #     terrain_colors = {
    #         0: (0, 0, 255),   # Water (Blue)
    #         1: (0, 255, 0),   # Plains (Green)
    #         2: (139, 69, 19), # Hills (Brown)
    #         3: (128, 128, 128), # Mountains (Gray)
    #         4: (34, 139, 34)  # Forest (Dark Green)
    #     }

    #     # Draw the terrain map
    #     # print("Visualizing terrain...")
    #     for i in range(self.height):
    #         for j in range(self.width):
    #             terrain_type = self.terrain_map[i, j]
    #             color = terrain_colors.get(terrain_type, (255, 255, 255))
    #             pygame.draw.rect(self.screen, color, (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

    # def visualize_civilizations(self):
    #     """Visualize the civilizations on the terrain map."""
    #     # print("Visualizing civilizations...")
    #     for civ in self.civilizations:
    #         x, y = civ.location
    #         pygame.draw.circle(self.screen, (255, 0, 0), (y * self.cell_size + self.cell_size // 2, 
    #                                                       x * self.cell_size + self.cell_size // 2), self.cell_size // 3)

    # def update_display(self):
    #     """Update the display to show the latest visualization."""
    #     pygame.display.flip()

    # def run_visualization(self):
    #     """Run the visualization loop."""
    #     running = True
    #     while running:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 running = False

    #         self.screen.fill((255, 255, 255))
    #         self.visualize_terrain()
    #         self.visualize_civilizations()
    #         self.update_display()

    #     pygame.quit()

    def start_simulation(self):
        """Run the full simulation and include visualization."""
        self.print_intro()

        # Set development mode parameters
        if self.dev_mode:
            Civilization.default_R = int(min(Civilization.map.width, Civilization.map.height) * 1)
            print("Using development mode with R for all civs being:", Civilization.default_R)

        # Generate civilizations
        self.generate_civilizations()
        
        print (Civilization.Civilizations[-1].cultural_context)

        # Run the simulation
        self.progress_simulation()

        # ****************** TO DO ****************** #
        #             Run the visualization           #
        #            self.run_visualization()         #
        # ******************************************* #

    def end_simulation(self):
        """End the simulation and analyze and create charts."""
        # Analyze and create charts
        self.analyze_artifacts()
        self.create_charts()

if __name__ == "__main__":
    simulations = 5
    civs = 3
    ages = 8
    increasing = False
    speed_multiplier = 8

    for simulation in range(simulations):
        print(f"\nStarting simulation #{simulation + 1} with {civs} civilizations and {ages} ages...\n")
        simulation = CulturaSimulation(civs=civs, dev_mode=True, ages=ages,speed_multiplier=speed_multiplier)
        simulation.start_simulation()

        # print("\n\n\n")
        # for civ in Civilization.Civilizations:
        #     print(f"{civ.cultural_context}\n")
        #     print(f"History: \n    {civ.string_history}\n")
        #     print(f"Neighbor History: \n    {civ.string_neighbor_history}\n")

        if increasing:
            civs += 1
            ages = ages ** 2
    simulation.end_simulation()
