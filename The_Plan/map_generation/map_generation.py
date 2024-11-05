import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2

# Map settings
width, height = 200, 200  # Size of the map
scale = 40.0              # Scale for Perlin noise
octaves = 6               # Number of noise layers
persistence = 0.5         # Amplitude control
lacunarity = 2.0          # Frequency control

# Generate the height map using Perlin noise
def generate_height_map(width, height, scale, octaves, persistence, lacunarity):
    height_map = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            height_map[i][j] = pnoise2(
                i / scale, j / scale, octaves=octaves, 
                persistence=persistence, lacunarity=lacunarity, 
                repeatx=width, repeaty=height, base=42
            )
    return height_map

# Normalize the height map
def normalize_map(height_map):
    min_val = np.min(height_map)
    max_val = np.max(height_map)
    normalized_map = (height_map - min_val) / (max_val - min_val)
    return normalized_map

# Classify terrain into different types based on height
def classify_terrain(normalized_map):
    terrain_map = np.zeros_like(normalized_map)
    for i in range(normalized_map.shape[0]):
        for j in range(normalized_map.shape[1]):
            if normalized_map[i][j] < 0.3:
                terrain_map[i][j] = 0  # Water (oceans, lakes)
            elif 0.3 <= normalized_map[i][j] < 0.5:
                terrain_map[i][j] = 1  # Plains
            elif 0.5 <= normalized_map[i][j] < 0.7:
                terrain_map[i][j] = 2  # Hills
            else:
                terrain_map[i][j] = 3  # Mountains
    return terrain_map

# Generate and classify the map
height_map = generate_height_map(width, height, scale, octaves, persistence, lacunarity)
normalized_map = normalize_map(height_map)
terrain_map = classify_terrain(normalized_map)

# Visualize the map with colors for different terrain types
plt.figure(figsize=(12, 12))
terrain_colors = {
    0: 'blue',       # Water
    1: 'lightgreen', # Plains
    2: 'sienna',     # Hills
    3: 'white'       # Mountains
}
cmap_terrain = plt.imshow(normalized_map, cmap='terrain', interpolation='bicubic')
plt.colorbar(cmap_terrain, label='Height')
plt.title('Procedurally Generated 2D World Map with Natural Features', fontsize=18)

# Overlay terrain classification
for i in range(height):
    for j in range(width):
        if terrain_map[i][j] == 0:  # Water
            plt.scatter(j, i, color='blue', s=1)  # Blue dots for water
        elif terrain_map[i][j] == 3:  # Mountains
            plt.scatter(j, i, color='white', s=1)  # White dots for mountains

plt.show()
