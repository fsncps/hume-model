from textual.widgets import Markdown
from typing import List, Dict
import math


class MomentsWidget(Markdown):
    """
    A Markdown widget that displays theoretical moments (mean, std dev, variance)
    for each variable across all iterations of the simulation state.
    """

    def on_mount(self) -> None:
        self.current_markdown = ""  # Used for export
        self.app.log(f"[MomentsWidget] Mounted with size={self.size}")

    def compute_mean(self, values: List[float]) -> float:
        return sum(values) / len(values) if values else 0.0

    def compute_variance(self, values: List[float]) -> float:
        mean = self.compute_mean(values)
        return sum((x - mean) ** 2 for x in values) / len(values) if values else 0.0

    def compute_stddev(self, values: List[float]) -> float:
        return math.sqrt(self.compute_variance(values)) if values else 0.0

    def update_from_simulation(self, state: List[Dict[str, float]]) -> None:
        """
        Generate and display a markdown table of moments from simulation data.
        """
        self.app.log("[MomentsWidget] update_from_simulation called.")
        self.app.log(f"[MomentsWidget] Received state with {len(state)} iterations.")

        if not state:
            self.app.log("[MomentsWidget] State is empty, showing fallback message.")
            self.current_markdown = "*No data available yet.*"
            self.update(self.current_markdown)
            return

        keys = state[0].keys()
        rows = [
            "| Variable | Mean     | Std. Dev. | Variance |",
            "|----------|----------|-----------|----------|"
        ]

        for key in keys:
            values = [row[key] for row in state if key in row]
            mean = self.compute_mean(values)
            std = self.compute_stddev(values)
            var = self.compute_variance(values)
            self.app.log(f"[MomentsWidget] {key}: mean={mean:.5f}, std={std:.5f}, var={var:.5f}")
            rows.append(f"| {key:8} | {mean:.5f} | {std:.5f}   | {var:.5f}  |")

        self.current_markdown = "\n".join(rows)
        self.app.log("[MomentsWidget] Generated Markdown Table:\n" + self.current_markdown)
        self.update(self.current_markdown)

    def get_data_as_dicts(self) -> List[Dict[str, float]]:
        """
        Parse the current markdown table back into a list of dicts for export.
        """
        lines = self.current_markdown.splitlines()
        data = []

        for line in lines[2:]:  # Skip header and divider
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) == 4:
                try:
                    data.append({
                        "variable": parts[0],
                        "mean": float(parts[1]),
                        "std_dev": float(parts[2]),
                        "variance": float(parts[3]),
                    })
                except ValueError:
                    self.app.log(f"[MomentsWidget] Skipped malformed row: {line}")
        return data

