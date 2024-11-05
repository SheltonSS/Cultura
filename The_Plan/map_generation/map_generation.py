import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2

# Map settings
width, height = 200, 200  # Increase map size for more detail
scale = 40.0              # Adjust scale for better patterns
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
plt.figure(figsize=(12, 12))
plt.imshow(normalized_map, cmap='terrain', interpolation='bicubic')  # Apply bicubic interpolation for smoothness
plt.colorbar(label='Height')
plt.title('Enhanced Procedurally Generated 2D World Map', fontsize=18)

# Add contour lines for elevation effect
contour = plt.contour(normalized_map, levels=15, colors='black', linewidths=0.5)
plt.clabel(contour, inline=True, fontsize=8, fmt='%.2f')

# Add gridlines
plt.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.5)

plt.show()
