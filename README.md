# Cultura
Cultura leverages NLP and procedural generation to create cultural artifacts that reflect the evolution and diversity of civilizations. Using historical and linguistic data, Cultura generates texts that embody cultural shifts over time. The project explores how computational models can simulate nuanced cultural identities.

# Workflow Overview-------------------------------------

Step 1: Data Acquisition
  Datasets Used:
    Historical texts, artifacts, and linguistic stuff relevant to the civilizations being studied.
    Publicly available datasets, such as Project Gutenberg for historical texts and cultural datasets from academic repositories.

Step 2: Preprocessing
Preprocessing Steps:
  Data cleaning (removing noise, irrelevant entries).
  Tokenization and normalization of text.
  Annotation and tagging of linguistic features.
  Filtering the dataset to focus on specific time periods or cultural aspects.
  
Step 3: Model Selection and Fine-Tuning
Model Used:
  GPT2
Fine-Tuning:
  fine-tuned on the preprocessed dataset to adapt to the specific cultural contexts.

Step 4: Generating Outputs using NLP Scholar
  Run the model in the generation mode to create cultural artifacts based on input parameters such as time period or cultural theme.
  Collect generated outputs (texts, symbols, etc.) for evaluation.

Step 5: Evaluation of Model Performance
  Perplexity: Measure how well the model predicts the next word.
  BLEU Score: Compare the generated text with reference texts for linguistic similarity.
  Human evaluation: Gather qualitative feedback from domain experts on cultural authenticity and relevance.

Step 6: Analyzing Results
  Success Criteria:
    High BLEU scores and low perplexity indicate the model generates culturally relevant artifacts.
  Negative Results:
    If outputs lack authenticity or fail to capture cultural nuances, this may indicate the need for more diverse training data or model adjustments.
      Conclusion from Negative Results:
        Insights gained from failures can guide further refinement of the model and preprocessing steps, ensuring improved cultural representation in future iterations.






