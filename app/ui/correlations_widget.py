from textual.widgets import Markdown
from typing import List, Dict
import math


class CorrelationsWidget(Markdown):
    """
    A Markdown widget that displays a correlation matrix for all variables
    across all iterations of the simulation state.
    """

    def on_mount(self) -> None:
        self.current_markdown = ""  # ✅ used for export
        self.app.log(f"[CorrelationsWidget] Mounted with size={self.size}")

    def compute_mean(self, values: List[float]) -> float:
        return sum(values) / len(values) if values else 0.0

    def compute_stddev(self, values: List[float]) -> float:
        mean = self.compute_mean(values)
        return math.sqrt(sum((x - mean) ** 2 for x in values) / len(values)) if values else 0.0

    def compute_correlation(self, x: List[float], y: List[float]) -> float:
        if not x or not y or len(x) != len(y):
            return 0.0

        mean_x = self.compute_mean(x)
        mean_y = self.compute_mean(y)
        std_x = self.compute_stddev(x)
        std_y = self.compute_stddev(y)

        if std_x == 0 or std_y == 0:
            return 0.0  # Avoid divide-by-zero

        cov = sum((a - mean_x) * (b - mean_y) for a, b in zip(x, y)) / len(x)
        return cov / (std_x * std_y)

    def update_from_simulation(self, state: List[Dict[str, float]]) -> None:
        self.app.log("[CorrelationsWidget] update_from_simulation called.")
        self.app.log(f"[CorrelationsWidget] Received state with {len(state)} iterations.")

        if not state:
            self.app.log("[CorrelationsWidget] State is empty, showing fallback message.")
            self.current_markdown = "*No data available yet.*"
            self.update(self.current_markdown)
            return

        keys = list(state[0].keys())
        value_map = {key: [row[key] for row in state if key in row] for key in keys}

        # Build table rows
        header = "|        | " + " | ".join(f"{k:>8}" for k in keys) + " |"
        divider = "|" + ("--------|" * (len(keys) + 1))
        rows = [header, divider]

        for k1 in keys:
            row = [f"{k1:>8}"]
            for k2 in keys:
                corr = self.compute_correlation(value_map[k1], value_map[k2])
                row.append(f"{corr:>8.3f}")
                self.app.log(f"[CorrelationsWidget] corr({k1}, {k2}) = {corr:.5f}")
            rows.append("| " + " | ".join(row) + " |")

        self.current_markdown = "\n".join(rows)
        self.app.log("[CorrelationsWidget] Generated Correlation Matrix:\n" + self.current_markdown)
        self.update(self.current_markdown)

    def get_data_as_matrix(self) -> Dict[str, Dict[str, float]]:
        """
        Parse the markdown table back into a nested dict structure for export.
        """
        lines = self.current_markdown.splitlines()
        if len(lines) < 3:
            return {}

        headers = [h.strip() for h in lines[0].split("|")[2:-1]]  # skip first col and trailing "|"
        matrix = {}

        for line in lines[2:]:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= len(headers) + 1:
                row_var = parts[0]
                values = parts[1:1 + len(headers)]
                matrix[row_var] = {}
                for col, val in zip(headers, values):
                    try:
                        matrix[row_var][col] = float(val)
                    except ValueError:
                        matrix[row_var][col] = 0.0
                        self.app.log(f"[CorrelationsWidget] Skipped malformed value in row '{row_var}': {val}")
        return matrix

