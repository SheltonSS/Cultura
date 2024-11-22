import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2
import random
from scipy.ndimage import gaussian_filter
from matplotlib.colors import ListedColormap

class TerrainMap:
    def __init__(self, width=200, height=200, base_scale=40.0, octaves=6, persistence=0.5, lacunarity=2.0, seed=None):
        self.width = width
        self.height = height
        self.base_scale = base_scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.seed = seed or random.randint(1, 250)
        self.height_map = None
        self.normalized_map = None
        self.terrain_map = None
    
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
        
        # Tundra at the poles
        # terrain_map[:20, :] = 5  # Tundra at the top
        # terrain_map[-20:, :] = 5  # Tundra at the bottom
        
        self.terrain_map = terrain_map

    def generate(self, smooth_sigma=3):
        """Generate the terrain map by chaining all the steps."""
        self.generate_height_map()
        self.normalize_map()
        self.smooth_map(sigma=smooth_sigma)
        self.classify_terrain()
    
    def visualize(self):
        """Visualize the terrain map."""
        cmap = ListedColormap([
            (0.2, 0.4, 0.8),  # Water - blue
            (0.5, 0.8, 0.4),  # Plains - green
            (0.6, 0.5, 0.2),  # Hills - brown
            (0.5, 0.5, 0.5),  # Mountains - gray
            (0.2, 0.6, 0.3),  # Forests - dark green
            # (0.7, 0.9, 0.9)   # Tundra - light blue
        ])

        plt.figure(figsize=(10, 10))
        plt.imshow(self.terrain_map, cmap=cmap, interpolation='bicubic')
        plt.colorbar(label='Terrain Features')
        plt.title(f'Procedurally Generated 2D World Map (Seed: {self.seed})')
        plt.show()

# Example usage
if __name__ == "__main__":
    terrain = TerrainMap(width=400, height=400)
    terrain.generate(smooth_sigma=3)
    terrain.visualize()
