import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2

# Map settings
width, height = 100, 100  # Size of the map
scale = 20.0              # Scale for the Perlin noise
octaves = 6               # Number of layers of noise
persistence = 0.5         # Determines the amplitude of octaves
lacunarity = 2.0          # Controls frequency of octaves

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

# Normalize the height map for better visualization
def normalize_map(height_map):
    min_val = np.min(height_map)
    max_val = np.max(height_map)
    normalized_map = (height_map - min_val) / (max_val - min_val)
    return normalized_map

# Generate and normalize the map
height_map = generate_height_map(width, height, scale, octaves, persistence, lacunarity)
normalized_map = normalize_map(height_map)

# Visualize the map using matplotlib
plt.figure(figsize=(10, 10))
plt.imshow(normalized_map, cmap='terrain')  # Use 'terrain' colormap for better effect
plt.colorbar(label='Height')
plt.title('Procedurally Generated 2D World Map')
plt.show()
