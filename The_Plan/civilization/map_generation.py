import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2
import random
from scipy.ndimage import gaussian_filter
from matplotlib.colors import ListedColormap

class TerrainMap:
    def __init__(self, width=25, height=25, base_scale=40.0, octaves=6, persistence=0.5, lacunarity=2.0, seed=None):
        self.width = width
        self.height = height
        self.base_scale = base_scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        # self.seed = seed or random.randint(1, 250)
        self.seed =21
        self.height_map = None
        self.normalized_map = None
        self.terrain_map = None
        self.forest_map = None

        self.create_terrain_map()
    
    def generate_height_map(self):
        """Generate a Perlin noise-based height map."""
        x_indices = np.arange(self.height) / self.base_scale
        y_indices = np.arange(self.width) / self.base_scale
        x_grid, y_grid = np.meshgrid(x_indices, y_indices, indexing='ij')

        self.height_map = np.vectorize(lambda x, y: pnoise2(
            x, y, octaves=self.octaves, persistence=self.persistence, 
            lacunarity=self.lacunarity, repeatx=self.width, repeaty=self.height, 
            base=self.seed
        ))(x_grid, y_grid)
    
    def normalize_map(self):
        """Normalize the height map to a range of [0, 1]."""
        self.normalized_map = (self.height_map - np.min(self.height_map)) / (np.max(self.height_map) - np.min(self.height_map))
    
    def smooth_map(self, sigma=2):
        """Smooth the normalized map to create more cohesive features.""" 
        self.normalized_map = gaussian_filter(self.normalized_map, sigma=sigma)
    
    def classify_terrain(self):
        """Classify the terrain based on the normalized height map."""
        terrain_map = np.zeros_like(self.normalized_map, dtype=int)
        terrain_map[self.normalized_map < 0.3] = 0  # Water
        terrain_map[(self.normalized_map >= 0.3) & (self.normalized_map < 0.6)] = 1  # Plains
        terrain_map[(self.normalized_map >= 0.6) & (self.normalized_map < 0.7)] = 2  # Hills
        terrain_map[self.normalized_map >= 0.7] = 3  # Mountains
        self.terrain_map = terrain_map
    
    def generate_forests(self, forest_probability=0.1, min_forest_size=5, max_forest_size=15):
        """Generate forests on the map with a limited number and specific size, avoiding mountains."""
        forest_map = np.zeros_like(self.normalized_map, dtype=int)

        # Only consider plains and hills for forest placement
        possible_positions = np.where((self.terrain_map == 1) | (self.terrain_map == 2))

        # Randomly select a number of positions to generate forests
        num_forests = int(len(possible_positions[0]) * forest_probability)
        
        for _ in range(num_forests):
            # Pick a random starting point from the possible positions (plains and hills only)
            start_idx = random.randint(0, len(possible_positions[0]) - 1)
            start_x = possible_positions[0][start_idx]
            start_y = possible_positions[1][start_idx]

            # Randomly determine the size of the forest patch
            forest_size = random.randint(min_forest_size, max_forest_size)
            
            # Create an irregular, organic shape for the forest
            forest_cells = [(start_x, start_y)]
            visited = set(forest_cells)
            direction_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

            # Grow the forest by expanding in random directions
            while len(forest_cells) < forest_size:
                new_cells = []
                for x, y in forest_cells:
                    random.shuffle(direction_offsets)  # Randomize direction
                    for dx, dy in direction_offsets:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.height and 0 <= ny < self.width:
                            if self.terrain_map[nx, ny] != 3 and (nx, ny) not in visited:  # Avoid mountains
                                new_cells.append((nx, ny))
                                visited.add((nx, ny))

                if new_cells:
                    forest_cells.extend(new_cells[:forest_size - len(forest_cells)])

            # Mark forest cells in the forest map
            for x, y in forest_cells:
                forest_map[x, y] = 4  # Mark as forest
        
        self.forest_map = forest_map

    def generate(self, smooth_sigma=3, forest_probability=0.1):
        """Generate the terrain map by chaining all the steps."""
        self.generate_height_map()
        self.normalize_map()
        self.smooth_map(sigma=smooth_sigma)
        self.classify_terrain()
        self.generate_forests(forest_probability)

    def visualize(self):
        """Visualize the terrain map."""
        cmap = ListedColormap([
            (0.2, 0.4, 0.8),  # Water - blue
            (0.5, 0.8, 0.4),  # Plains - green
            (0.6, 0.5, 0.2),  # Hills - brown
            (0.5, 0.5, 0.5),  # Mountains - gray
            (0.2, 0.6, 0.3),  # Forests - dark green
        ])

        # Combine the terrain and forest maps
        combined_map = np.copy(self.terrain_map)
        combined_map[self.forest_map == 4] = 4  # Forests take precedence over other terrain types

        plt.figure(figsize=(10, 10))
        plt.imshow(combined_map, cmap=cmap, interpolation='bicubic')
        plt.colorbar(label='Terrain Features')
        plt.title(f'Procedurally Generated 2D World Map (Seed: {self.seed})')
        plt.show()

    def get_terrain_map(self):
        # for row in self.terrain_map:
        #     print(row)
        return self.terrain_map
    def create_terrain_map(self):
        self.generate(smooth_sigma=3, forest_probability=0.05)
        self.get_terrain_map()
        return self.terrain_map

# Example usage
# if __name__ == "__main__":
#     terrain = TerrainMap()
#     terrain.visualize()
#     terrain.generate(smooth_sigma=3, forest_probability=0.05)  # Adjust forest probability to control density
#     terrain.get_terrain_map()
#     terrain.visualize()
