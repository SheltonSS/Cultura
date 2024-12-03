from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from joblib import Parallel, delayed
import json
import config

class ArtifactAnalyzer:
    def __init__(self, model_name='all-MiniLM-L6-v2', artifact_file='artifact.jsonl', analyzed_file='analyzed_artifacts.jsonl', Civilization_Class=None):
        self.model = SentenceTransformer(model_name)
        self.artifact_file = artifact_file
        self.analyzed_file = analyzed_file
        self.Civilization_Class = Civilization_Class
        self.existing_artifacts = self.load_artifacts()

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

    def save_artifacts(self, artifacts):
        """Save artifacts to a specified JSONL file."""
        def convert_to_serializable(obj):
            """Convert non-serializable objects to JSON-compatible types."""
            if isinstance(obj, (np.float32, np.float64, float)):
                return float(obj)
            elif isinstance(obj, (np.int32, np.int64, int)):
                return int(obj)
            elif isinstance(obj, (np.ndarray, list)):
                return obj.tolist()
            return obj

        serializable_artifacts = [json.loads(json.dumps(artifact, default=convert_to_serializable)) for artifact in artifacts]
        print(f" Saving artifacts: {serializable_artifacts}")
        try:
            with open(self.analyzed_file, 'w') as file:
                for artifact in serializable_artifacts:
                    file.write(json.dumps(artifact) + '\n')
        except Exception as e:
            print(f"Error saving artifacts: {e}")

    def clear_artifact_file(self):
        """Wipes the artifact file clean but leaves the analyzed file intact.""" 
        open(self.artifact_file, 'w').close()

    def calculate_narrative_integration(self, artifact, civ):
        """Calculate the narrative integration score between the artifact and civilization history."""
        artifact_description = artifact.get('Description', '').strip()
        if not artifact_description:
            print("Artifact description is missing or empty.")
            return 0.0

        try:
            artifact_embedding = self.model.encode(artifact_description)
        except Exception as e:
            print(f"Error encoding artifact description: {e}")
            return 0.0

        history = civ.neighbor_history if artifact.get("generation_type") == "neighbor" else civ.history
        if not history or not isinstance(history, list):
            print("Civilization history is missing or invalid.")
            return 0.0

        narrative = " ".join(history).strip()
        if not narrative:
            print("Civilization history is empty after combining.")
            return 0.0

        try:
            narrative_embedding = self.model.encode(narrative)
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

        keywords = [str(kw).lower() for kw in traits + biome + techlvl]
        matched_keywords = [kw for kw in keywords if kw in artifact_description.lower()]

        accuracy = len(matched_keywords) / len(keywords) if keywords else 0
        return accuracy, matched_keywords

    def calculate_novelty(self, artifact_description):
        """Calculates the novelty score of the artifact description against existing artifacts."""
        if not self.existing_artifacts:
            return 1.0, []

        artifact_embedding = self.model.encode(artifact_description)
        existing_embeddings = self.model.encode([artifact['Description'] for artifact in self.existing_artifacts])

        similarities = [cosine_similarity([artifact_embedding], [emb])[0][0] for emb in existing_embeddings]
        novelty_score = 1 - np.mean(similarities)
        return novelty_score, similarities

    def cumulative_analysis_score(self, artifact, narrative_weight=0.335, accuracy_weight=0.2, novelty_weight=0.465):
        """Calculate a cumulative score for the artifact based on narrative, cultural accuracy, and novelty."""
        civ_name = artifact.get('Civilization Name')
        civ = self.Civilization_Class.Civilizations_by_name.get(civ_name)
        if not civ:
            print(f"Civilization {civ_name} not found.")
            return {
                "narrative_integration": 0.0,
                "cultural_accuracy": 0.0,
                "novelty_score": 0.0,
                "cumulative_score": 0.0,
                "matched_keywords": []
            }

        narrative_integration = self.calculate_narrative_integration(artifact, civ)
        cultural_accuracy, matched_keywords = self.calculate_cultural_accuracy(artifact['Description'], civ)
        novelty_score, _ = self.calculate_novelty(artifact['Description'])

        normalized_narrative_integration = (narrative_integration + 1) / 2
        cumulative_score = (normalized_narrative_integration * narrative_weight +
                            cultural_accuracy * accuracy_weight +
                            novelty_score * novelty_weight)

        return {
            "narrative_integration": narrative_integration,
            "cultural_accuracy": cultural_accuracy,
            "novelty_score": novelty_score,
            "cumulative_score": cumulative_score,
            "matched_keywords": matched_keywords
        }

    def analyze_artifact(self, artifact):
        """Analyze a single artifact."""
        if 'cumulative_score' in artifact:
            return artifact

        scores = self.cumulative_analysis_score(artifact)
        artifact.update(scores)

        print(f"Artifact Analysis Scores:")
        print(f"Narrative Integration: {scores['narrative_integration']}")
        print(f"Cultural Accuracy: {scores['cultural_accuracy']}")
        print(f"Novelty Score: {scores['novelty_score']}")
        print(f"Cumulative Score: {scores['cumulative_score']}\n")

        return artifact

    def analyze_artifacts(self, artifacts=None):
        """Analyze artifacts and ensure they persist after the program completes."""
        artifacts = artifacts or self.existing_artifacts
        analyzed_artifacts = [self.analyze_artifact(artifact) for artifact in artifacts]

        try:
            with open(self.analyzed_file, 'a') as file:
                for artifact in analyzed_artifacts:
                    # Convert the artifact to a serializable format
                    def convert_to_serializable(obj):
                        """Convert non-serializable objects to JSON-compatible types."""
                        if isinstance(obj, (np.float32, np.float64, float)):
                            return float(obj)
                        elif isinstance(obj, (np.int32, np.int64, int)):
                            return int(obj)
                        elif isinstance(obj, (np.ndarray, list)):
                            return obj.tolist()
                        return obj

                    serializable_artifact = json.dumps(artifact, default=convert_to_serializable)
                    file.write(serializable_artifact + '\n')

        except Exception as e:
            print(f"Error saving artifacts: {e}")
            return None

        # Calculate the average cumulative score from the analyzed artifacts
        average_score = np.mean([artifact['cumulative_score'] for artifact in analyzed_artifacts])
        self.clear_artifact_file()
        return average_score
