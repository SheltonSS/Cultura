import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json

class ArtifactCharts:
    def __init__(self, analyzed_file='analyzed_artifacts.jsonl', output_dir='charts'):
        self.analyzed_file = analyzed_file
        self.output_dir = output_dir
        self.artifacts = self.load_artifacts()

    def load_artifacts(self):
        """Load analyzed artifacts from a JSONL file."""
        artifacts = []
        try:
            with open(self.analyzed_file, 'r') as file:
                for line in file:
                    artifact = json.loads(line)
                    artifacts.append(artifact)
        except FileNotFoundError:
            print(f"Error: File {self.analyzed_file} not found.")
        return artifacts

    def artifacts_to_dataframe(self):
        """Convert the list of artifacts to a Pandas DataFrame."""
        return pd.DataFrame(self.artifacts)

    def save_plot(self, fig, filename):
        """Save a plot as an image file in the output directory."""
        import os
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Chart saved to {filepath}")

    def plot_cumulative_score_distribution(self):
        """Plot the distribution of cumulative scores."""
        df = self.artifacts_to_dataframe()

        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.histplot(df["cumulative_score"], kde=True, bins=20, color="blue", alpha=0.7)
        plt.title("Distribution of Cumulative Scores", fontsize=16)
        plt.xlabel("Cumulative Score", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)

        self.save_plot(plt.gcf(), "cumulative_score_distribution.png")

    def plot_narrative_vs_accuracy(self):
        """Scatter plot of narrative integration vs. cultural accuracy."""
        df = self.artifacts_to_dataframe()

        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            x="narrative_integration", 
            y="cultural_accuracy", 
            hue="generation_type", 
            palette="viridis", 
            data=df
        )
        plt.title("Narrative Integration vs. Cultural Accuracy", fontsize=16)
        plt.xlabel("Narrative Integration", fontsize=12)
        plt.ylabel("Cultural Accuracy", fontsize=12)
        plt.legend(title="Generation Type")

        self.save_plot(plt.gcf(), "narrative_vs_accuracy.png")

    def plot_novelty_trend(self):
        """Line plot of novelty scores over time."""
        df = self.artifacts_to_dataframe()
        df = df.sort_values(by="generation_time")

        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.lineplot(x="generation_time", y="novelty_score", hue="generation_type", data=df, marker="o")
        plt.title("Novelty Score Trend Over Time", fontsize=16)
        plt.xlabel("Generation Time", fontsize=12)
        plt.ylabel("Novelty Score", fontsize=12)
        plt.legend(title="Generation Type")

        self.save_plot(plt.gcf(), "novelty_trend.png")

    def plot_metrics_by_generation_type(self):
        """Bar plots to compare metrics across generation types."""
        df = self.artifacts_to_dataframe()
        metrics = ["narrative_integration", "cultural_accuracy", "novelty_score", "cumulative_score"]

        sns.set(style="whitegrid")
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()

        for i, metric in enumerate(metrics):
            sns.barplot(
                x="generation_type", 
                y=metric, 
                data=df, 
                palette="viridis", 
                ax=axes[i],
                ci=None
            )
            axes[i].set_title(f"{metric.replace('_', ' ').title()} by Generation Type", fontsize=14)
            axes[i].set_xlabel("Generation Type", fontsize=12)
            axes[i].set_ylabel(metric.replace('_', ' ').title(), fontsize=12)

        plt.tight_layout()
        self.save_plot(fig, "metrics_by_generation_type.png")

    def generate_all_charts(self):
        """Generate and save all charts."""
        self.plot_cumulative_score_distribution()
        self.plot_narrative_vs_accuracy()
        # self.plot_novelty_trend()
        self.plot_metrics_by_generation_type()

if __name__ == "__main__":
    charts = ArtifactCharts()
    charts.generate_all_charts()
