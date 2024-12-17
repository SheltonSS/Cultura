from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from joblib import Parallel, delayed
import json
import config

class ArtifactAnalyzer:
    def __init__(self, model_name='all-MiniLM-L6-v2', artifact_file='artifact.jsonl',
                 analyzed_file='analyzed_artifacts.jsonl', Civilization_Class=None):
        self.model = SentenceTransformer(model_name)
        self.artifact_file = artifact_file
        self.analyzed_file = analyzed_file
        self.Civilization_Class = Civilization_Class
        self.existing_artifacts = self.load_artifacts(self.artifact_file)
        self.previously_analyzed = self.load_artifacts(self.analyzed_file)

    @staticmethod
    def load_artifacts(jsonl_file):
        """Load artifacts from a JSONL file."""
        artifacts = []
        try:
            with open(jsonl_file, 'r') as file:
                artifacts = [json.loads(line) for line in file]
        except FileNotFoundError:
            print(f"Warning: {jsonl_file} not found. Starting fresh.")
        return artifacts

    @staticmethod
    def save_artifacts(artifacts, jsonl_file):
        """Save artifacts to a JSONL file in a serializable format."""
        def convert_to_serializable(obj):
            """Convert non-serializable objects to JSON-compatible types."""
            if isinstance(obj, (np.float32, np.float64, float)):
                return float(obj)
            elif isinstance(obj, (np.int32, np.int64, int)):
                return int(obj)
            elif isinstance(obj, (np.ndarray, list)):
                return obj.tolist()
            return obj

        with open(jsonl_file, 'w') as file:
            for artifact in artifacts:
                serializable_artifact = json.dumps(artifact, default=convert_to_serializable)
                file.write(serializable_artifact + '\n')

    def clear_artifact_file(self):
        """Wipes the artifact file clean but leaves the analyzed file intact."""
        open(self.artifact_file, 'w').close()

    def calculate_narrative_integration(self, artifact, civ):
        """Calculate the narrative integration score between the artifact and civilization history."""
        description = " ".join([
            artifact.get('Name', ''),
            artifact.get('Description', ''),
            artifact.get('Purpose', '')
        ]).strip()

        if not description:
            return 0.0

        try:
            artifact_embedding = self.model.encode(description)
            history = civ.neighbor_history if artifact.get("generation_type") == "neighbor" else civ.history
            narrative = " ".join(history).strip()
            narrative_embedding = self.model.encode(narrative)
            return cosine_similarity([artifact_embedding], [narrative_embedding])[0][0]
        except Exception as e:
            print(f"Error calculating narrative integration: {e}")
            return 0.0

    def calculate_cultural_accuracy(self, artifact_description, civ):
        """Calculates cultural accuracy based on traits, biome, and technology."""
        traits = civ.traits
        techlvl = [config.Tech_eras[civ.tech_level]]
        biome = [civ.terrain_type]

        keywords = [str(kw).lower() for kw in traits + biome + techlvl]
        matched_keywords = [kw for kw in keywords if kw in artifact_description.lower()]
        accuracy = len(matched_keywords) / len(keywords) if keywords else 0
        return accuracy, matched_keywords

    def calculate_novelty(self, artifact_description):
        """Calculates novelty score by comparing with previously analyzed artifacts."""
        if not self.previously_analyzed:
            return 1.0, []

        try:
            artifact_embedding = self.model.encode(artifact_description)
            previous_descriptions = [artifact['Description'] for artifact in self.previously_analyzed]
            previous_embeddings = self.model.encode(previous_descriptions)
            similarities = [cosine_similarity([artifact_embedding], [emb])[0][0] for emb in previous_embeddings]
            novelty_score = 1 - np.mean(similarities)
            return novelty_score, similarities
        except Exception as e:
            print(f"Error calculating novelty: {e}")
            return 1.0, []

    def cumulative_analysis_score(self, artifact, narrative_weight=0.335, accuracy_weight=0.2, novelty_weight=0.465):
        """Combine scores for narrative integration, cultural accuracy, and novelty."""
        civ_name = artifact.get('Civilization Name')
        civ = self.Civilization_Class.Civilizations_by_name.get(civ_name)

        if not civ:
            print(f"Error: Civilization '{civ_name}' not found.")
            return {"narrative_integration": 0.0, "cultural_accuracy": 0.0, "novelty_score": 0.0,
                    "cumulative_score": 0.0, "matched_keywords": []}

        description = " ".join([
            artifact.get('Name', ''),
            artifact.get('Description', ''),
            artifact.get('Purpose', '')
        ]).strip()

        narrative_integration = self.calculate_narrative_integration(artifact, civ)
        cultural_accuracy, matched_keywords = self.calculate_cultural_accuracy(description, civ)
        novelty_score, _ = self.calculate_novelty(description)

        # Normalize narrative score to [0, 1]
        normalized_narrative = (narrative_integration + 1) / 2
        cumulative_score = (normalized_narrative * narrative_weight +
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
        print(f"\nArtifact '{artifact.get('Name', 'Unknown')}':")
        for key, value in scores.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        return artifact

    def analyze_artifacts(self, artifacts=None, parallel=False):
        """Analyze all artifacts, optionally in parallel, and save results."""
        artifacts = artifacts or self.existing_artifacts
        analyze_fn = self.analyze_artifact

        if parallel:
            analyzed_artifacts = Parallel(n_jobs=-1)(delayed(analyze_fn)(artifact) for artifact in artifacts)
        else:
            analyzed_artifacts = [analyze_fn(artifact) for artifact in artifacts]

        self.save_artifacts(analyzed_artifacts, self.analyzed_file)
        avg_score = np.mean([artifact['cumulative_score'] for artifact in analyzed_artifacts])
        self.clear_artifact_file()
        return avg_score
