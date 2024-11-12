import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2
import random
from scipy.ndimage import gaussian_filter

# Map settings
width, height = 200, 200  # Map size
base_scale = 50.0         # Base scale for noise
octaves = 6               # Number of layers of noise
persistence = 0.5         # Amplitude of octaves
lacunarity = 2.0          # Frequency of octaves
river_width = 3           # Width of rivers
lake_count = 5            # Number of lakes
seed = random.randint(100, 999)                # Controlled seed for consistency

# Generate the height map with Perlin noise and controlled seed
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

    # Apply Gaussian blur to smooth the noise, grouping high areas naturally
    height_map = gaussian_filter(height_map, sigma=1.5)
    return height_map

# Normalize the height map
def normalize_map(height_map):
    return (height_map - np.min(height_map)) / (np.max(height_map) - np.min(height_map))

# Classify terrain types with smoother transitions
def classify_terrain(normalized_map):
    terrain_map = np.zeros_like(normalized_map, dtype=int)
    terrain_map[normalized_map < 0.3] = 0  # Water
    terrain_map[(normalized_map >= 0.3) & (normalized_map < 0.5)] = 1  # Plains
    terrain_map[(normalized_map >= 0.5) & (normalized_map < 0.7)] = 2  # Hills
    terrain_map[normalized_map >= 0.7] = 3  # Mountains
    return terrain_map

# Generate rivers with smoother pathing
def generate_rivers(terrain_map, width, height, river_width):
    rivers_map = np.copy(terrain_map)
    river_start_points = [(random.randint(0, width-1), 0), (random.randint(0, width-1), height-1)]

    for x, y in river_start_points:
        for i in range(height):
            if x < 0 or x >= width or y < 0 or y >= height: 
                break
            rivers_map[x, y] = 0  # Water
            x += random.choice([-1, 0, 1])
            y += 1
            x = max(0, min(x, width - 1))
            y = max(0, min(y, height - 1))

    return rivers_map

# Generate lakes with grouped low elevation spots
def generate_lakes(terrain_map, width, height, lake_count):
    lakes_map = np.copy(terrain_map)
    for _ in range(lake_count):
        lake_x, lake_y = random.randint(10, width - 10), random.randint(10, height - 10)
        lake_radius = random.randint(4, 8)
        for i in range(lake_x - lake_radius, lake_x + lake_radius):
            for j in range(lake_y - lake_radius, lake_y + lake_radius):
                if (i - lake_x)**2 + (j - lake_y)**2 <= lake_radius**2:
                    if 0 <= i < width and 0 <= j < height:
                        lakes_map[i, j] = 0  # Water
    return lakes_map

# Group forest areas for better clustering
def generate_forests_and_biomes(terrain_map):
    forest_map = np.copy(terrain_map)
    for i in range(1, terrain_map.shape[0] - 1):
        for j in range(1, terrain_map.shape[1] - 1):
            if (terrain_map[i, j] in [1, 2] and
                np.random.rand() > 0.7 and
                np.count_nonzero(terrain_map[i-1:i+2, j-1:j+2] == 4) > 1):
                forest_map[i, j] = 4  # Forests on plains and hills with neighbors

    return forest_map

# Generate and classify the map
height_map = generate_height_map(width, height, base_scale, octaves, persistence, lacunarity, seed)
normalized_map = normalize_map(height_map)
terrain_map = classify_terrain(normalized_map)

# Add rivers, lakes, and forests
rivers_map = generate_rivers(terrain_map, width, height, river_width)
lakes_map = generate_lakes(terrain_map, width, height, lake_count)
forest_map = generate_forests_and_biomes(terrain_map)

# Combine maps for visualization
combined_map = np.maximum(np.maximum(rivers_map, lakes_map), forest_map)

# Visualize the map
plt.figure(figsize=(10, 10))
plt.imshow(combined_map, cmap='terrain', interpolation='bicubic')
plt.colorbar(label='Terrain Features')
plt.title(f'Procedurally Generated 2D World Map with Natural Features (Seed: {seed})')
plt.show()
