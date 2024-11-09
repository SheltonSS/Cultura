import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2
import random

# Map settings
width, height = 100, 100  # Map size
base_scale = 40.0         # Base scale for noise
octaves = 8               # Number of layers of noise
persistence = 0.5         # Amplitude of octaves
lacunarity = 2.0          # Frequency of octaves
river_width = 3           # Width of rivers
lake_count = 5            # Number of lakes

# Generate the height map using Perlin noise with a controlled seed for natural results
def generate_height_map(width, height, scale, octaves, persistence, lacunarity, seed=None):
    if seed is None:
        # Control seed to avoid extremes, keep it within a certain range
        seed = random.randint(100, 999)

    # Adjust the map by using a scaled seed to prevent too much variance
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

# Classify terrain types for a natural look
def classify_terrain(normalized_map):
    terrain_map = np.zeros_like(normalized_map, dtype=int)
    terrain_map[normalized_map < 0.3] = 0  # Water
    terrain_map[(normalized_map >= 0.3) & (normalized_map < 0.5)] = 1  # Plains
    terrain_map[(normalized_map >= 0.5) & (normalized_map < 0.7)] = 2  # Hills
    terrain_map[normalized_map >= 0.7] = 3  # Mountains
    return terrain_map

# Generate rivers (paths of low elevation)
def generate_rivers(terrain_map, width, height, river_width):
    rivers_map = np.copy(terrain_map)
    river_start_points = [(random.randint(0, width-1), 0), (random.randint(0, width-1), height-1)]  # Start at top or bottom

    for x, y in river_start_points:
        # Generate the path of the river
        for i in range(height):
            if x < 0 or x >= width or y < 0 or y >= height: 
                break  # If out of bounds, stop the river generation

            rivers_map[x, y] = 0  # Set as water
            
            # Move the river in random direction within bounds
            x += random.choice([-1, 0, 1])  # Move left, right, or stay
            y += 1  # Move downward
            
            # Ensure x stays within bounds
            x = max(0, min(x, width - 1))
            # Ensure y stays within bounds
            y = max(0, min(y, height - 1))

    return rivers_map


# Generate lakes (low elevation surrounded by terrain)
def generate_lakes(terrain_map, width, height, lake_count):
    lakes_map = np.copy(terrain_map)
    for _ in range(lake_count):
        lake_x, lake_y = random.randint(10, width - 10), random.randint(10, height - 10)
        lake_radius = random.randint(4, 8)  # Random radius for lake
        # Set circular lake areas as water
        for i in range(lake_x - lake_radius, lake_x + lake_radius):
            for j in range(lake_y - lake_radius, lake_y + lake_radius):
                if (i - lake_x)**2 + (j - lake_y)**2 <= lake_radius**2:  # Circular area
                    if 0 <= i < width and 0 <= j < height:
                        lakes_map[i, j] = 0  # Set as water
    return lakes_map

# Forests and Biomes
def generate_forests_and_biomes(terrain_map):
    forest_map = np.copy(terrain_map)
    # Forests are often found on plains or hills, we can simulate this
    forest_map[(terrain_map == 1) & (np.random.rand(*terrain_map.shape) > 0.7)] = 4  # Forests on plains
    forest_map[(terrain_map == 2) & (np.random.rand(*terrain_map.shape) > 0.5)] = 4  # Forests on hills
    
    return forest_map

# Generate and classify the map
# seed = random.randint(0, 255)  # Control seed within a reasonable range
seed = 104
height_map = generate_height_map(width, height, base_scale, octaves, persistence, lacunarity, seed)
normalized_map = normalize_map(height_map)
terrain_map = classify_terrain(normalized_map)

# Add rivers, lakes, and forests
rivers_map = generate_rivers(terrain_map, width, height, river_width)
lakes_map = generate_lakes(terrain_map, width, height, lake_count)
forest_map = generate_forests_and_biomes(terrain_map)

# Combine maps (rivers and lakes over terrain)
combined_map = np.maximum(np.maximum(rivers_map, lakes_map), forest_map)

# Visualize the map with terrain classification
plt.figure(figsize=(10, 10))
plt.imshow(combined_map, cmap='terrain', interpolation='bicubic')
plt.colorbar(label='Terrain Features')
plt.title(f'Procedurally Generated 2D World Map with Natural Features (Seed: {seed})')
plt.show()
