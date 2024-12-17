import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
from pandas.plotting import parallel_coordinates
import itertools


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

    def artifacts_to_dataframe(self, type="all"):
        """Convert the list of artifacts to a Pandas DataFrame."""
        if type == "all":
            return pd.DataFrame(self.artifacts)
        elif type == "history":
            return pd.DataFrame([artifact for artifact in self.artifacts if artifact["generation_type"] == "history"])
        elif type == "neighbor":
            return pd.DataFrame([artifact for artifact in self.artifacts if artifact["generation_type"] == "neighbor"])

    def save_plot(self, fig, filename):
        """Save a plot as an image file in the output directory."""
        import os
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Chart saved to {filepath}")

    @staticmethod
    def clean_label(label):
        """Convert labels like 'narrative_integration' to 'Narrative Integration'."""
        return label.replace('_', ' ').title()

    def plot_cumulative_score_distribution(self, type="all"):
        """Plot the distribution of cumulative scores for the specified artifact type."""
        df = self.artifacts_to_dataframe(type)

        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.histplot(df["cumulative_score"], kde=True, bins=20, color="blue", alpha=0.7)
        plt.title(f"Distribution of Cumulative Scores ({type.capitalize()})", fontsize=16)
        plt.xlabel(self.clean_label("cumulative_score"), fontsize=12)
        plt.ylabel("Frequency", fontsize=12)

        self.save_plot(plt.gcf(), f"cumulative_score_distribution_{type}.png")

    def plot_narrative_vs_accuracy(self, type="all"):
        """Scatter plot of narrative integration vs. cultural accuracy for the specified artifact type."""
        df = self.artifacts_to_dataframe(type)

        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            x="narrative_integration",
            y="cultural_accuracy",
            hue="generation_type",
            palette={"history": "lightblue", "neighbor": "lightgreen"},
            data=df
        )
        plt.title(f"{self.clean_label('narrative_integration')} vs. {self.clean_label('cultural_accuracy')} ({type.capitalize()})", fontsize=16)
        plt.xlabel(self.clean_label("narrative_integration"), fontsize=12)
        plt.ylabel(self.clean_label("cultural_accuracy"), fontsize=12)
        plt.legend(title="Generation Type")

        self.save_plot(plt.gcf(), f"narrative_vs_accuracy_{type}.png")

    def plot_metrics_by_generation_type(self, type="all"):
        """Bar plots to compare metrics across generation types for the specified artifact type."""
        df = self.artifacts_to_dataframe(type)
        metrics = ["narrative_integration", "cultural_accuracy", "novelty_score", "cumulative_score"]

        palette = {"history": "lightblue", "neighbor": "lightgreen"}

        sns.set(style="whitegrid")
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()

        for i, metric in enumerate(metrics):
            sns.barplot(
                x="generation_type",
                y=metric,
                data=df,
                ax=axes[i],
                palette=palette,
                errorbar=None
            )
            axes[i].set_title(f"{self.clean_label(metric)} by Generation Type ({type.capitalize()})", fontsize=14)
            axes[i].set_xlabel("Generation Type", fontsize=12)
            axes[i].set_ylabel(self.clean_label(metric), fontsize=12)

        plt.tight_layout()
        self.save_plot(fig, f"metrics_by_generation_type_{type}.png")

    def plot_multi_metric_comparison(self, type="all"):
        """Create a parallel coordinates plot to compare multiple metrics."""
        df = self.artifacts_to_dataframe(type)

        metrics = ["narrative_integration", "cultural_accuracy", "novelty_score"]
        df_subset = df[metrics + ["generation_type"]]

        plt.figure(figsize=(12, 8))
        parallel_coordinates(df_subset, "generation_type", color=["blue", "green"], alpha=0.7, linewidth=1.5)

        plt.title(f"Multi-Metric Comparison ({type.capitalize()})", fontsize=16)
        plt.xlabel("Metrics", fontsize=12)
        plt.ylabel("Values", fontsize=12)
        plt.legend(title="Generation Type", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)

        self.save_plot(plt.gcf(), f"multi_metric_comparison_{type}.png")

    def plot_metric_combinations(self, type="all"):
        """Generate scatter plots comparing every combination of two metrics with trend lines."""
        df = self.artifacts_to_dataframe(type)

        metrics = ["narrative_integration", "cultural_accuracy", "novelty_score", "cumulative_score"]
        combinations = list(itertools.combinations(metrics, 2))

        sns.set(style="whitegrid")
        n_combinations = len(combinations)
        n_cols = 2
        n_rows = (n_combinations + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 6 * n_rows))
        axes = axes.flatten()

        for i, (metric_x, metric_y) in enumerate(combinations):
            ax = axes[i]
            sns.scatterplot(
                x=metric_x,
                y=metric_y,
                hue="generation_type",
                data=df,
                ax=ax,
                palette={"history": "lightblue", "neighbor": "lightgreen"},
                alpha=0.8,
            )
            sns.regplot(
                x=metric_x,
                y=metric_y,
                data=df,
                scatter=False,
                ax=ax,
                color="red",
                line_kws={"linewidth": 1.5},
            )
            ax.set_title(f"{self.clean_label(metric_x)} vs. {self.clean_label(metric_y)} ({type.capitalize()})")
            ax.set_xlabel(self.clean_label(metric_x))
            ax.set_ylabel(self.clean_label(metric_y))
            ax.legend(title="Generation Type", loc="best", fontsize="small")

        for i in range(len(combinations), len(axes)):
            fig.delaxes(axes[i])

        plt.tight_layout()
        self.save_plot(fig, f"metric_combinations_{type}.png")

    def generate_all_charts(self):
        """Generate all charts for all artifact types."""
        types = ["all", "history", "neighbor"]

        for artifact_type in types:
            print(f"Generating charts for {artifact_type} artifacts...")
            self.plot_cumulative_score_distribution(type=artifact_type)
            self.plot_narrative_vs_accuracy(type=artifact_type)
            self.plot_metrics_by_generation_type(type=artifact_type)
            self.plot_multi_metric_comparison(type=artifact_type)
            self.plot_metric_combinations(type=artifact_type)

        print("All charts have been generated and saved.")


if __name__ == "__main__":
    charts = ArtifactCharts()
    charts.generate_all_charts()
