from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from joblib import Parallel, delayed
import json
import config

class ArtifactAnalyzer:
    def __init__(self, model_name='all-MiniLM-L6-v2', artifact_file='artifact.jsonl', Civilization_Class=None):
        """Initializes the ArtifactAnalyzer with a SentenceTransformer model."""
        self.model = SentenceTransformer(model_name)
        self.artifact_file = artifact_file
        self.Civilization_Class = Civilization_Class
        self.existing_artifacts = self.load_artifacts()

    def calculate_narrative_integration(self, artifact, civ):
        """
        Calculates narrative integration between an artifact description and a civilization's history or neighbor history."""
        # Extract artifact description
        artifact_description = artifact.get('Description', '').strip()
        if not artifact_description:
            print("Artifact description is missing or empty.")
            return 0.0

        # Attempt to encode the artifact description
        try:
            artifact_embedding = self.model.encode(artifact_description)
        except Exception as e:
            print(f"Error encoding artifact description: {e}")
            return 0.0

        # Determine the appropriate history (regular or neighbor)
        history = civ.neighbor_history if artifact.get("generation_type") == "neighbor" else civ.history
        if not history or not isinstance(history, list):
            print("Civilization history is missing, empty, or invalid.")
            return 0.0

        # Combine the history into a single narrative string
        narrative = " ".join(history).strip()
        if not narrative:
            print("Civilization history is empty after combining.")
            return 0.0

        # Attempt to encode the civilization narrative
        try:
            narrative_embedding = self.model.encode(narrative)
        except Exception as e:
            print(f"Error encoding civilization history: {e}")
            return 0.0

        # Calculate cosine similarity
        try:
            similarity = cosine_similarity([artifact_embedding], [narrative_embedding])[0][0]
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0

        return similarity


    def calculate_cultural_accuracy(self, artifact_description, civ):
        """Calculates cultural accuracy based on the alignment of an artifact description with the cultural profile."""
        traits = civ.traits
        techlvl = [config.Tech_eras[civ.tech_level]]
        biome = [civ.terrain_type]

        keywords = traits + biome + techlvl
        matched_keywords = [str(kw).lower() for kw in keywords if str(kw).lower() in artifact_description.lower()]

        accuracy = len(matched_keywords) / len(keywords) if keywords else 0
        return accuracy, matched_keywords

    def load_artifacts(self):
        """Load artifacts from a JSONL file."""
        artifacts = []
        try:
            with open(self.artifact_file, 'r') as file:
                for line in file:
                    artifact = json.loads(line)
                    artifacts.append(artifact)
        except FileNotFoundError:
            print(f"Error: File {self.artifact_file} not found.")
        return artifacts

    def save_artifacts(self):
        """Save the updated artifacts back to the JSONL file."""
        with open(self.artifact_file, 'w') as file:
            for artifact in self.existing_artifacts:
                file.write(json.dumps(artifact) + '\n')

    def calculate_novelty(self, artifact_description):
        """
        Calculates the novelty of an artifact by comparing it with existing artifacts.
        """
        if not self.existing_artifacts:
            print("No existing artifacts to compare against.")
            return 1.0, []

        # Generate embeddings for the artifact and existing artifacts
        artifact_embedding = self.model.encode(artifact_description)
        existing_embeddings = self.model.encode([artifact['Description'] for artifact in self.existing_artifacts])

        # Calculate similarities using cosine similarity
        similarities = Parallel(n_jobs=-1)(
            delayed(cosine_similarity)([artifact_embedding], [emb]) for emb in existing_embeddings
        )
        similarities = np.array(similarities).flatten()

        novelty_score = 1 - np.mean(similarities)
        return novelty_score, similarities

    def cumulative_analysis_score(self, artifact, narrative_weight=0.33, accuracy_weight=0.33, novelty_weight=0.34):
        """
        Calculates the cumulative analysis score by combining narrative integration, cultural accuracy, and novelty.
        
        Returns a dictionary with individual scores and the final cumulative score.
        """
        # Calculate narrative integration
        narrative_integration = self.calculate_narrative_integration(artifact, self.Civilization_Class.Civilizations_by_name[artifact['Civilization Name']])
        
        # Calculate cultural accuracy
        cultural_accuracy, matched_keywords = self.calculate_cultural_accuracy(artifact['Description'], self.Civilization_Class.Civilizations_by_name[artifact['Civilization Name']])
        
        # Calculate novelty
        novelty_score, similarities = self.calculate_novelty(artifact['Description'])

        # Normalize scores (if needed)
        normalized_narrative_integration = (narrative_integration + 1) / 2
        normalized_cultural_accuracy = cultural_accuracy
        normalized_novelty_score = novelty_score  

        # Calculate cumulative score
        cumulative_score = (normalized_narrative_integration * narrative_weight +
                            normalized_cultural_accuracy * accuracy_weight +
                            normalized_novelty_score * novelty_weight)

        # Return individual scores and cumulative score
        return {
            "narrative_integration": narrative_integration,
            "cultural_accuracy": cultural_accuracy,
            "novelty_score": novelty_score,
            "cumulative_score": cumulative_score,
            "matched_keywords": matched_keywords
        }

    def analyze_artifact(self, artifact):
        """Analyze a single artifact, and save the result to the artifact object if not already analyzed."""
        # Check if the artifact has already been analyzed
        if 'cumulative_score' in artifact:
            print(f"Skipping artifact '{artifact['Name']}' as it is already analyzed.")
            return artifact  # Skip this artifact if it already has a cumulative score

        # Calculate the cumulative score and add it to the artifact object
        cumulative_score = self.cumulative_analysis_score(artifact)
        artifact['cumulative_score'] = cumulative_score
        artifact['narrative_integration'] = cumulative_score['narrative_integration']
        artifact['cultural_accuracy'] = cumulative_score['cultural_accuracy']
        artifact['novelty_score'] = cumulative_score['novelty_score']
        artifact['matched_keywords'] = cumulative_score['matched_keywords']

        for key in artifact['cumulative_score'].keys():
            print(f"{key}: {artifact['cumulative_score'][key]}")
        print()

        # Save the updated artifact list back to the JSONL file
        self.save_artifacts()

        return artifact

    def analyze_artifacts(self, artifacts):
        """Analyze multiple artifacts and return the average cumulative score."""
        total_score = 0
        analyzed_artifacts = 0

        # Analyze each artifact
        for artifact in artifacts:
            result = self.analyze_artifact(artifact)
            total_score += result['cumulative_score']['cumulative_score']
            analyzed_artifacts += 1

        average_score = total_score / analyzed_artifacts if analyzed_artifacts else 0
        return average_score



# Example usage
# if __name__ == "__main__":
#     analyzer = ArtifactAnalyzer()

#     # Example data
#     artifact_description = "A golden chalice symbolizing peace, used in sacred rituals."
#     civilization_narrative = "This is a peaceful society that values harmony and sacred rituals."
#     cultural_profile = {
#         "traits": ['Expansive', 'Communal', 'Expansive', 'Expansive', 'Communal', 'Expansive', 'Ambitious', 'Communal', 'Altruistic', 'Expansive'],
#         "materials": ["gold", "silver"],
#         "technologies": ["bronze casting", "pottery"]
#     }
#     existing_artifacts = [
#         "A silver goblet used in peace ceremonies.",
#         "A bronze sword forged for battle.",
#         "An ornate vase used for offerings."
#     ]

#     # Narrative Integration
#     narrative_score = analyzer.calculate_narrative_integration(artifact_description, civilization_narrative)
#     print("Narrative Integration Score:", narrative_score)

#     # Cultural Accuracy
#     cultural_accuracy_score, matched_keywords = analyzer.calculate_cultural_accuracy(artifact_description, cultural_profile)
#     print("Cultural Accuracy Score:", cultural_accuracy_score)
#     print("Matched Keywords:", matched_keywords)

#     # Novelty
#     novelty_score, similarities = analyzer.calculate_novelty(artifact_description, existing_artifacts)
#     print("Novelty Score:", novelty_score)
#     print("Similarities with Existing Artifacts:", similarities)
