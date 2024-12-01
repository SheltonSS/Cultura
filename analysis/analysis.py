from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# load model
model = SentenceTransformer('all-MiniLM-L6-v2')  # lightweight model for embeddings

# =====================================Function to calculate narrative integration=====================================
def calculate_narrative_integration(artifact_description, civilization_narrative):
    # embeddings
    artifact_embedding = model.encode(artifact_description)
    narrative_embedding = model.encode(civilization_narrative)

    # cosine similarity
    similarity = cosine_similarity([artifact_embedding], [narrative_embedding])[0][0]
    return similarity

# example input
artifact_description = "A golden chalice symbolizing peace, used in sacred rituals."
civilization_narrative = "This is a peaceful society that values harmony and sacred rituals."

# calculate narrative integration
score = calculate_narrative_integration(artifact_description, civilization_narrative)
print("Narrative Integration Score:", score)

# # =====================================Function to calculate cultural accuracy=====================================
# def calculate_cultural_accuracy(artifact_description, cultural_profile):
#     # Simple keyword matching for cultural traits
#     traits = cultural_profile.get("traits", [])
#     materials = cultural_profile.get("materials", [])
#     technologies = cultural_profile.get("technologies", [])
    
#     keywords = traits + materials + technologies
#     matched_keywords = [kw for kw in keywords if kw.lower() in artifact_description.lower()]
    
#     # Score based on the percentage of matched keywords
#     accuracy = len(matched_keywords) / len(keywords) if keywords else 0
#     return accuracy, matched_keywords

# # Example input
# artifact_description = "A golden chalice symbolizing peace, used in sacred rituals."
# cultural_profile = {
#     "traits": ["peace", "harmony", "sacred rituals"],
#     "materials": ["gold", "silver"],
#     "technologies": ["bronze casting", "pottery"]
# }

# # Calculate cultural accuracy
# score, matched_keywords = calculate_cultural_accuracy(artifact_description, cultural_profile)
# print("Cultural Accuracy Score:", score)
# print("Matched Keywords:", matched_keywords)

# # =====================================Function to calculate novelty=====================================
# # Database of existing artifacts (descriptions)
# existing_artifacts = [
#     "A silver goblet used in peace ceremonies.",
#     "A bronze sword forged for battle.",
#     "An ornate vase used for offerings."
# ]

# def calculate_novelty(artifact_description, existing_artifacts):
#     # Generate embeddings for all artifacts
#     artifact_embedding = model.encode(artifact_description)
#     existing_embeddings = model.encode(existing_artifacts)

#     # Calculate similarity with all existing artifacts
#     similarities = cosine_similarity([artifact_embedding], existing_embeddings)[0]
    
#     # Novelty is 1 - average similarity
#     novelty_score = 1 - np.mean(similarities)
#     return novelty_score, similarities

# # Example input
# artifact_description = "A golden chalice symbolizing peace, used in sacred rituals."

# # Calculate novelty
# novelty_score, similarities = calculate_novelty(artifact_description, existing_artifacts)
# print("Novelty Score:", novelty_score)
# print("Similarities with Existing Artifacts:", similarities)

