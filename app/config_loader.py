# app/config_loader.py

from pathlib import Path
import tomllib

CONFIG_PATH = Path(__file__).parent / "config.toml"

def load_config(path: Path = CONFIG_PATH) -> dict:
    """
    Load and return the TOML config as a dictionary.
    
    Args:
        path (Path): Path to the TOML config file.

    Returns:
        dict: Parsed config.
    """
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "rb") as f:
        return tomllib.load(f)

