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
    # Practical and Survival Artifacts
    "Weapon", 
    "Armor",
    "Tool",
    "Cooking Utensil",
    "Farming Implement",
    "Hunting Gear",
    "Navigation Instrument",
    "Utility Device",

    # Literary and Oral Tradition
    "Saying",
    "Proverb",
    "Fable",
    "Legend",
    "Epic Tale",
    "Myth",
    "Historical Account",
    "Riddle",
    "Chant",
    "Lullaby",
    "Story Scroll",
    
    # Personal Adornments and Clothing
    "Jewelry",
    "Clothing or Garb",
    "Headdress",
    "Mask",
    "Footwear",
    "Cloak or Robe",

    # Musical and Performance Artifacts
    "Musical Instrument",
    "Songbook",
    "Sheet Music",
    "Dance Prop",
    "Stage Decoration",

    # Religious and Spiritual Artifacts
    "Religious Artifact",
    "Altar",
    "Totem",
    "Prayer Bead",
    "Sacred Text",
    "Ritual Tool",
    "Amulet",
    "Talisman",
    "Divination Tool",

    # Visual and Sculptural Artifacts
    "Sculpture",
    "Visual Art",
    "Performance Art",
    "Painting",
    "Mask Art",
    "Relief",
    "Carving",
    "Mosaic",
    "Tapestry",
    "Engraving",

    # Written and Spoken Artifacts
    "Poem",
    "Song",
    "Inscription",
    "Manuscript",
    "Charter",
    "Edict",
    "Scroll",

    # Architectural and Monumental Artifacts
    "Mural",
    "Building",
    "Monument",
    "Bridge",
    "Temple",
    "Aqueduct",
    "Fortification",
    "Statue",

    # Trade and Craft Artifacts
    "Trade Good",
    "Pottery",
    "Basket",
    "Glasswork",
    "Metalwork",
    "Textile",
    "Dyed Fabric",
    "Coinage",
    "Barter Token",

    # Miscellaneous and Unique Artifacts
    "Map",
    "Flag",
    "Banner",
    "Seal",
    "Crest",
    "Cultural Recipe",
    "Game Piece",
    "Puzzle",
    "Calendar",
    "Clock",
    "Mechanical Invention",
    "Scientific Instrument"
]


test_terrain = [
    [1, 1, 0, 3, 5],
    [1, 2, 2, 3, 5],
    [0, 1, 1, 2, 5],
]


# 0: (0, 0, 255),   # Water (Blue)
# 1: (0, 255, 0),   # Plains (Green)
# 2: (139, 69, 19), # Hills (Brown)
# 3: (128, 128, 128), # Mountains (Gray)
# 4: (34, 139, 34)  # Forest (Dark Green)

base_traits = {
    0: [  # Water
        "Skilled Mariners", "Coastal Survivors", "Ocean Navigators", 
        "Expert Fishers", "Trade Route Explorers", "Storm Resilient", 
        "Seafaring Innovators", "Tide Predictors", "Efficient Resource Harvesters"
    ],
    1: [  # Plains
        "Experienced Farmers", "Grassland Guardians", "Community Gatherers", 
        "Agricultural Ritualists", "Nature Harmonizers", "Wide-Open Wanderers", 
        "Nomadic Herdsmen", "Weather-Adapted Crops", "Crop Cultivators"
    ],
    2: [  # Hills
        "Terraced Farmers", "Hilltop Defenders", "Mountain Raiders", 
        "Erosion Engineers", "Innovative Builders", "Miner Experts", 
        "Terrain Specialists", "Hillside Traders", "Efficient Engineers"
    ],
    3: [  # Mountains
        "Summit Defenders", "Mountain Survivors", "Fortress Builders", 
        "Cold-Weather Foragers", "Defense Strategists", "Stone Craftsmen", 
        "Mountain Pathfinders", "Self-Sufficient Nomads", "Alpine Warriors"
    ],
    4: [  # Forest
        "Tree Dwellers", "Experienced Foragers", "Woodland Keepers", 
        "Nature Worshippers", "Stealthy Hunters", "Woodworkers", 
        "Mystical Trailblazers", "Bark Artisans", "Forest Guardians"
    ],
    5: [  # Tundra
        "Frost Survivors", "Ice Explorers", "Snow Seekers", 
        "Scarcity Adapters", "Winter Foragers", "Arctic Pathfinders", 
        "Tundra Shamans", "Beast Trainers", "Frozen Terrain Experts"
    ]
}



cmap = ListedColormap([
    (0.2, 0.4, 0.8),  # Water - blue
    (0.5, 0.8, 0.4),  # Plains - green
    (0.6, 0.5, 0.2),  # Hills - brown
    (0.5, 0.5, 0.5),  # Mountains - gray
    (0.2, 0.6, 0.3),  # Forests - dark green
])

civ_names = [
    "Aetheris",
    "Sylvannor",
    "Caelorith",
    "Xylarion",
    "Korrathian",
    "Velkor",
    "Zevryth",
    "Falnor",
    "Zythar Empire",
    "Tharvokh League",
    "Eryndrial Ascendancy",
    "Otharion Hegemony",
    "Vyrlithian Pact",
    "Luminaris Covenant",
    "Ashendor Sovereignty",
    "Pyrrithan Expanse",
    "Draventh Concord",
    "Qirath Theocracy",
    "Myrrhan League",
    "Brynthar Imperium"
]

Cvilization_Class_config = {
    "Event_Limit": 5, 
    "Neighbor_Interaction_Limit": 5, 
    "Starting_Year":-4000,
    "Year_Progression": 50,
    "Speed_Multiplier": 1,
    "Dev_Mode": False
}