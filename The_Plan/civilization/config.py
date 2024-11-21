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
    purpose
    Description 
    Significance
"""

artifact_types = [
    "Weapon", "Tool", "Ceremonial Object", "Clothing", "Instrument", 
    "Religious Artifact", "Artwork", "Writing", "Trade Good"
]

terrain_map = [
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