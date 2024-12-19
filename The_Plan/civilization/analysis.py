from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from joblib import Parallel, delayed
import json
import config
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from sentence_transformers import SentenceTransformer, util
import string

from nltk.corpus import wordnet

nltk.download('stopwords')
nltk.download('wordnet')
# Make it so that the artifact's cultural accuracy is based on the civs traits at the time of the artifact's creation instead of the civs traits at end of the game

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
        """Append new artifacts to a JSONL file in a serializable format."""
        def convert_to_serializable(obj, seen=None):
            """Convert non-serializable objects to JSON-compatible types."""
            if seen is None:
                seen = set()
            
            obj_id = id(obj)
            if obj_id in seen:
                return "Circular Reference Detected"
            
            seen.add(obj_id)
            if isinstance(obj, (np.float32, np.float64, float)):
                return float(obj)
            elif isinstance(obj, (np.int32, np.int64, int)):
                return int(obj)
            elif isinstance(obj, (np.ndarray, list)):
                return [convert_to_serializable(o, seen) for o in obj]
            elif isinstance(obj, dict):
                return {k: convert_to_serializable(v, seen) for k, v in obj.items()}
            elif isinstance(obj, str):
                return obj
            return str(obj)
        
        with open(jsonl_file, 'a') as file:
            for artifact in artifacts:
                artifact.pop('Civilization Info', None)
                artifact.pop('Purpose', None)
                artifact.pop('Description', None)
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

    def calculate_cultural_accuracy(self, artifact_description, civ, civ_info):
        """Calculates cultural accuracy based on traits, biome, and technology with semantic similarity."""

        stop_words = set(stopwords.words('english'))

        # lemmatizer and stemmer for normalization
        lemmatizer = WordNetLemmatizer()
        stemmer = PorterStemmer()

        # semantic similarity model
        model = SentenceTransformer('all-MiniLM-L6-v2')

        # normalize words function
        def normalize_words(words):
            table = str.maketrans('', '', string.punctuation)
            return [
                lemmatizer.lemmatize(stemmer.stem(word.translate(table))).lower()
                for word in words
            ]

        # expand words with synonyms function
        def expand_with_synonyms(words):
            expanded_words = set()
            for word in words:
                expanded_words.add(word)
                for syn in wordnet.synsets(word):
                    for lemma in syn.lemmas():
                        expanded_words.add(lemma.name().lower())
            return list(expanded_words)

        # get civilization info
        traits = civ_info["Traits"]
        techlvl = [civ_info["Tech Level"]]
        biome = [civ_info["Region"]]
        history = civ_info["Civilization History"]

        # combine all keywords into a single list of words
        keywords = []
        keywords.extend([str(kw).lower() for kw in traits])
        keywords.extend([str(kw).lower() for kw in techlvl])
        keywords.extend([str(kw).lower() for kw in biome])
        keywords.extend(" ".join(history).lower().split())

        # remove stop words and normalize keywords
        keywords = [kw for kw in keywords if kw not in stop_words]
        keywords = normalize_words(keywords)

        # expand normalized keywords with synonyms
        keywords_with_synonyms = expand_with_synonyms(keywords)

        # split artifact description, remove stop words, and normalize
        artifact_words = artifact_description.lower().split()
        artifact_words = [word for word in artifact_words if word not in stop_words]
        artifact_words = normalize_words(artifact_words)

        # match normalized and expanded keywords in artifact description
        matched_keywords = [kw for kw in keywords_with_synonyms if kw in artifact_words]

        # semantic similarity check
        keyword_embeddings = model.encode(keywords_with_synonyms, convert_to_tensor=True)
        artifact_embedding = model.encode(artifact_description, convert_to_tensor=True)
        similarity_scores = util.cos_sim(keyword_embeddings, artifact_embedding)

        # threshold for considering a match
        threshold = 0.7
        semantic_matches = [
            keywords_with_synonyms[idx]
            for idx, score in enumerate(similarity_scores)
            if score > threshold
        ]

        # combine results
        total_matches = len(set(matched_keywords + semantic_matches))
        accuracy = total_matches / len(keywords_with_synonyms) if keywords_with_synonyms else 0

        return accuracy, set(matched_keywords + semantic_matches)

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

        artifact_description = " ".join([
            artifact.get('Name', ''),
            artifact.get('Description', ''),
            artifact.get('Purpose', '')
        ]).strip()

        civ_info = artifact.get('Civilization Info', '')
            
        narrative_integration = self.calculate_narrative_integration(artifact, civ)
        cultural_accuracy, matched_keywords = self.calculate_cultural_accuracy(artifact_description, civ,civ_info)
        novelty_score, _ = self.calculate_novelty(artifact_description)

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
