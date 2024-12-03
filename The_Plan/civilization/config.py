from matplotlib.colors import ListedColormap

Tech_eras_string ="""
Ancient
Classical
Medieval
Renaissance
Industrial
Modern
Atomic
Information
Future
"""

Tech_eras = Tech_eras_string.split("\n")[1:-1]
blank = ""
for i in range(len(Tech_eras)):
    blank+= f"    {i}:{Tech_eras[i]}\n"
blank = blank[:-1]
Tech_eras_string = blank
# print(Tech_eras)

json_format = """ 
    Name
    Description
    purpose
"""
# Museum_artifact_format = """
#     Name

artifact_types = [
    "Weapon", 
    "Armor",
    "Tool", 

    "Saying",
    "Proverb",
    "fable",
    "legend",  

    "Jewelry",
    "Clothing or Garb",  

    "Musical Instrument",

    "Religious Artifact", 

    "Sculpture",
    "Visual Art",
    "performance Art",

    "Poem",
    "song",

    "Mural",
    "Building",
    "Monument",

    "Dance",

    "Trade Good"
]

test_terrain = [
    [1, 1, 0, 3, 5],
    [1, 2, 2, 3, 5],
    [0, 1, 1, 2, 5],
]

base_traits = {
    0: ["Maritime", "Resourceful", "Nomadic"],  # Water
    1: ["Agrarian", "Peaceful", "Communal"],    # Plains
    2: ["Hardy", "Independent", "Resilient"],   # Hills
    3: ["Isolationist", "Strategic", "Defensive"],  # Mountains
    5: ["Adaptive", "Spiritual", "Tough"],      # Tundra
}

cmap = ListedColormap([
    (0.2, 0.4, 0.8),  # Water - blue
    (0.5, 0.8, 0.4),  # Plains - green
    (0.6, 0.5, 0.2),  # Hills - brown
    (0.5, 0.5, 0.5),  # Mountains - gray
    (0.2, 0.6, 0.3),  # Forests - dark green
])

civ_names = ["Shellenia", "Borfia", "Gantz", "Matopia", "Luzil", "Mattia", "Novia", "Okgot", "Gothia", "Galoria"]