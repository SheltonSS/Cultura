import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2
import random

# Map settings
width, height = 200, 200  # Size of the map
scale = random.uniform(20.0, 50.0)  
octaves = random.randint(4, 8)      
persistence = random.uniform(0.4, 0.6)
lacunarity = 2.0 

# Generate a random seed for unique map generation
random_seed = random.randint(0, 10000)

# Generate the height map using Perlin noise with vectorized operations
def generate_height_map(width, height, scale, octaves, persistence, lacunarity, base):
    x_indices = np.arange(height) / scale
    y_indices = np.arange(width) / scale
    x_grid, y_grid = np.meshgrid(x_indices, y_indices, indexing='ij')

    height_map = np.vectorize(lambda x, y: pnoise2(
        x, y, octaves=octaves, persistence=persistence, lacunarity=lacunarity,
        repeatx=width, repeaty=height, base=base
    ))(x_grid, y_grid)
    
    return height_map

# Normalize the height map using vectorized operations
def normalize_map(height_map):
    return (height_map - np.min(height_map)) / (np.max(height_map) - np.min(height_map))

# Classify terrain using vectorized operations
def classify_terrain(normalized_map):
    terrain_map = np.zeros_like(normalized_map, dtype=int)
    terrain_map[normalized_map < 0.3] = 0  # Water
    terrain_map[(normalized_map >= 0.3) & (normalized_map < 0.5)] = 1  # Plains
    terrain_map[(normalized_map >= 0.5) & (normalized_map < 0.7)] = 2  # Hills
    terrain_map[normalized_map >= 0.7] = 3  # Mountains
    return terrain_map

# Generate and classify the map
height_map = generate_height_map(width, height, scale, octaves, persistence, lacunarity, random_seed)
normalized_map = normalize_map(height_map)
terrain_map = classify_terrain(normalized_map)

# Visualize the map with colors for different terrain types
plt.figure(figsize=(10, 10))
plt.imshow(normalized_map, cmap='terrain', interpolation='bicubic')
plt.colorbar(label='Height')
plt.title('Randomly Generated 2D World Map with Natural Features')

plt.show()
