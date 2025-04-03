# app/utils/exporter.py

import csv
import os
from pathlib import Path
from datetime import datetime
from app.config_loader import load_config



def resolve_export_path(path_str: str | None) -> Path:
    """Resolve export path from config or fallbacks."""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    filename = f"hume_export-{timestamp}.csv"

    if path_str:
        path = Path(path_str).expanduser()
        if path.is_absolute():
            if path.is_dir() or str(path).endswith(("/", "\\")):  # ✅ explicitly a dir
                return path / filename
            return path.with_name(filename)

    # Fallback to XDG or APPDATA
    if os.name == "nt":
        base_dir = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base_dir = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))

    return base_dir / "hume-sim" / filename

def export_simulation(
    moments: list[dict[str, float]],
    correlations: dict[str, dict[str, float]],
    iterations: list[dict[str, float]]
) -> Path:
    config = load_config()
    configured_path = config.get("export", {}).get("path")
    export_path = resolve_export_path(configured_path)

    export_path.parent.mkdir(parents=True, exist_ok=True)

    with export_path.open("w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["=Moments="])
        if moments:
            keys = list(moments[0].keys())
            writer.writerow(keys)
            for row in moments:
                writer.writerow([row[k] for k in keys])
        writer.writerow([])

        writer.writerow(["=Correlations="])
        if correlations:
            headers = [""] + list(correlations.keys())
            writer.writerow(headers)
            for row_key, col_dict in correlations.items():
                row = [row_key] + [col_dict.get(k, "") for k in correlations.keys()]
                writer.writerow(row)
        writer.writerow([])

        writer.writerow(["=Iterations="])
        if iterations:
            keys = list(iterations[0].keys())
            writer.writerow(keys)
            for row in iterations:
                writer.writerow([row[k] for k in keys])

    return export_path

