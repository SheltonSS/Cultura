from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from joblib import Parallel, delayed

class ArtifactAnalyzer:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """Initializes the ArtifactAnalyzer with a SentenceTransformer model."""
         
        self.model = SentenceTransformer(model_name)
    
    def calculate_narrative_integration(self, artifact_description, civilization_narrative):
        """Calculates narrative integration between an artifact description and a civilization's narrative."""

        # Generate embeddings
        artifact_embedding = self.model.encode(artifact_description)
        narrative_embedding = self.model.encode(civilization_narrative)

        # Compute cosine similarity
        similarity = cosine_similarity([artifact_embedding], [narrative_embedding])[0][0]
        return similarity

    def calculate_cultural_accuracy(self, artifact_description, civ):
        """Calculates cultural accuracy based on the alignment of an artifact description with the cultural profile."""

        # traits = cultural_profile.get("traits", [])
        # materials = cultural_profile.get("materials", [])
        # technologies = cultural_profile.get("technologies", [])
        
        traits = civ.traits
        tech = civ.tech_level
        

        
        # Combine all keywords and match them with the artifact description
        keywords = traits + materials + technologies
        matched_keywords = [kw for kw in keywords if kw.lower() in artifact_description.lower()]
        
        # Calculate accuracy as the percentage of matched keywords
        accuracy = len(matched_keywords) / len(keywords) if keywords else 0
        return accuracy, matched_keywords

    def calculate_novelty(self, artifact_description, existing_artifacts):
        """
        Calculates the novelty of an artifact by comparing it with existing artifacts.

        Parameters:
        - artifact_description: str, the description of the artifact.
        - existing_artifacts: list of str, descriptions of existing artifacts.

        Returns:
        - float: novelty score between 0 and 1.
        - np.array: similarities with each existing artifact.
        """
        # Generate embeddings for the artifact and existing artifacts
        artifact_embedding = self.model.encode(artifact_description)
        existing_embeddings = self.model.encode(existing_artifacts)

        # Compute similarities
        # similarities = cosine_similarity([artifact_embedding], existing_embeddings)[0]
        similarities = Parallel(n_jobs=-1)(delayed(cosine_similarity)([artifact_embedding], [emb]) for emb in existing_embeddings)

        
        # Novelty is 1 - average similarity
        novelty_score = 1 - np.mean(similarities)
        return novelty_score, similarities

# Example usage
if __name__ == "__main__":
    analyzer = ArtifactAnalyzer()

    # Example data
    artifact_description = "A golden chalice symbolizing peace, used in sacred rituals."
    civilization_narrative = "This is a peaceful society that values harmony and sacred rituals."
    cultural_profile = {
        "traits": ["peace", "harmony", "sacred rituals"],
        "materials": ["gold", "silver"],
        "technologies": ["bronze casting", "pottery"]
    }
    existing_artifacts = [
        "A silver goblet used in peace ceremonies.",
        "A bronze sword forged for battle.",
        "An ornate vase used for offerings."
    ]

    # Narrative Integration
    narrative_score = analyzer.calculate_narrative_integration(artifact_description, civilization_narrative)
    print("Narrative Integration Score:", narrative_score)

    # Cultural Accuracy
    cultural_accuracy_score, matched_keywords = analyzer.calculate_cultural_accuracy(artifact_description, cultural_profile)
    print("Cultural Accuracy Score:", cultural_accuracy_score)
    print("Matched Keywords:", matched_keywords)

    # Novelty
    novelty_score, similarities = analyzer.calculate_novelty(artifact_description, existing_artifacts)
    print("Novelty Score:", novelty_score)
    print("Similarities with Existing Artifacts:", similarities)
