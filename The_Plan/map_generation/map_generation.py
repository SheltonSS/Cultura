import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2
import random
from scipy.ndimage import gaussian_filter
from matplotlib.colors import ListedColormap

# Map settings
width, height = 200, 200  # Map size
base_scale = 40.0         # Base scale for noise
octaves = 6               # Number of layers of noise
persistence = 0.5         # Amplitude of octaves
lacunarity = 2.0          # Frequency of octaves
river_width = 3           # Width of rivers
lake_count = 5            # Number of lakes

# Generate the height map using Perlin noise with a controlled seed for natural results
def generate_height_map(width, height, scale, octaves, persistence, lacunarity, seed=None):
    if seed is None:
        seed = random.randint(100, 999)

    x_indices = np.arange(height) / scale
    y_indices = np.arange(width) / scale
    x_grid, y_grid = np.meshgrid(x_indices, y_indices, indexing='ij')

    height_map = np.vectorize(lambda x, y: pnoise2(
        x, y, octaves=octaves, persistence=persistence, lacunarity=lacunarity,
        repeatx=width, repeaty=height, base=seed
    ))(x_grid, y_grid)
    
    return height_map

# Normalize the height map
def normalize_map(height_map):
    return (height_map - np.min(height_map)) / (np.max(height_map) - np.min(height_map))

# Smooth the map for larger feature grouping
def smooth_map(height_map, sigma=2):
    return gaussian_filter(height_map, sigma=sigma)

# Classify terrain types for a natural look, adding tundra at the poles
def classify_terrain(normalized_map):
    terrain_map = np.zeros_like(normalized_map, dtype=int)
    terrain_map[normalized_map < 0.3] = 0  # water
    terrain_map[(normalized_map >= 0.3) & (normalized_map < 0.5)] = 1  # Plains
    terrain_map[(normalized_map >= 0.5) & (normalized_map < 0.7)] = 2  # Hills
    terrain_map[normalized_map >= 0.7] = 3  # Mountains
    
    # Tundra at the poles (top and bottom rows of the map)
    terrain_map[:20, :] = 5  # Tundra at the top
    terrain_map[-20:, :] = 5  # Tundra at the bottom
    
    return terrain_map

# Generate rivers, lakes, and forests
# (Functions `generate_rivers`, `generate_lakes`, and `generate_forests_and_biomes` are unchanged)

# Generate the height map and classify terrain
seed = random.randint(1, 300)
height_map = generate_height_map(width, height, base_scale, octaves, persistence, lacunarity, seed)
normalized_map = normalize_map(smooth_map(height_map, sigma=3))  # Smooth with sigma=3 for more grouping
terrain_map = classify_terrain(normalized_map)

# Define colors for each terrain type
cmap = ListedColormap([
    (0.2, 0.4, 0.8),  # Water - blue
    (0.5, 0.8, 0.4),  # Plains - green
    (0.6, 0.5, 0.2),  # Hills - brown
    (0.5, 0.5, 0.5),  # Mountains - gray
    (0.2, 0.6, 0.3),  # Forests - dark green
    (0.7, 0.9, 0.9)   # Tundra - light blue
])

# Visualize the map with terrain classification
plt.figure(figsize=(10, 10))
plt.imshow(terrain_map, cmap=cmap, interpolation='bicubic')
plt.colorbar(label='Terrain Features')
plt.title(f'Procedurally Generated 2D World Map with Grouped Features (Seed: {seed})')
plt.show()
