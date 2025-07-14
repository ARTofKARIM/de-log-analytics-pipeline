"""Visualization for log analytics."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

class LogVisualizer:
    def __init__(self, output_dir="output/"):
        self.output_dir = output_dir

    def plot_status_distribution(self, status_dict, save=True):
        fig, ax = plt.subplots(figsize=(10, 5))
        codes = list(status_dict.keys())
        counts = list(status_dict.values())
        colors = ["#2ecc71" if c < 400 else "#e74c3c" if c >= 500 else "#f39c12" for c in codes]
        ax.bar([str(c) for c in codes], counts, color=colors)
        ax.set_xlabel("Status Code")
        ax.set_ylabel("Count")
        ax.set_title("HTTP Status Code Distribution")
        if save:
            fig.savefig(f"{self.output_dir}status_distribution.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    def plot_traffic_timeline(self, traffic_series, save=True):
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.plot(traffic_series.index, traffic_series.values, color="steelblue", linewidth=1.5)
        ax.fill_between(traffic_series.index, traffic_series.values, alpha=0.2, color="steelblue")
        ax.set_xlabel("Time")
        ax.set_ylabel("Requests")
        ax.set_title("Traffic Over Time")
        if save:
            fig.savefig(f"{self.output_dir}traffic_timeline.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    def plot_top_paths(self, paths_dict, n=10, save=True):
        fig, ax = plt.subplots(figsize=(10, 6))
        items = sorted(paths_dict.items(), key=lambda x: x[1], reverse=True)[:n]
        paths, counts = zip(*items) if items else ([], [])
        ax.barh(range(len(paths)), counts, color="steelblue")
        ax.set_yticks(range(len(paths)))
        ax.set_yticklabels(paths, fontsize=8)
        ax.set_title("Top Requested Paths")
        if save:
            fig.savefig(f"{self.output_dir}top_paths.png", dpi=150, bbox_inches="tight")
        plt.close(fig)
