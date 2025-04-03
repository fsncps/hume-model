# HumeSim — Interactive Economic Simulation

**HumeSim** is a lightweight, terminal-based economic simulation app built written in python and using [Textual](https://github.com/Textualize/textual) for its TUI. It is built for and used in conjunction with an academic paper on David Hume and his criticism of a prevalent mercantilist economic stance. It identifies a number of macroeconomic quantities and their functional relationships in Hume's *On Interest* and aims to model the trends and correlations for these variables in a dynamic simulation model.  It allows you to:

- Input initial endogenous macroeconomic variables, parameters and exogenous demand/supply shocks.
- Run dynamic iterations of the model.
- Manipulate values between each cycle iteration.
- View theoretical moments (mean, std. dev., variance) of all variables.
- Analyze Pearson correlation coefficient matrices between variables.
- Export results to a structured CSV.

---

## Requirements

- Python 3.12+
- `textual` (>= 0.45.0)
- `toml`


## Setup (Recommended)

Install Python 3.12 using your system’s package manager (apt, brew, etc.), or download the installer from python.org for Windows.

It's strongly recommended to use a virtual environment:

```bash
# Create a virtual environment (in .venv/)
python3 -m venv .venv

# Activate the virtual environment
# Linux/macOS:
source .venv/bin/activate
# Windows (CMD):
.venv\Scripts\activate.bat
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
```

## Running the App

After cloning the repo, run from within the repo root dir:

```bash
python -m app
```

## Configuration

The default config file is:

```
config.toml
```

In this file you can set the default values for all variables and the save path for the CSV export:

Example:
```toml
[defaults]
Y = 1.0       # Output
...

[parameters]
alpha = 0.33
...

[shocks]
A-mean = 1.0
...

[export]
path = "~/Documents/hume_exports/"  # relative or absolute path.
```

For Windows, an absolute path is required:
```toml
[export]
path = "C:\users\foo\bar\"  # full path
```

- If a directory is given, the export will be saved as:
  `hume_export-YYYY-MM-DD-HHMMSS.csv` inside that directory.
- If no path is configured, it defaults to:
  - Linux: `$XDG_DATA_HOME/hume-sim/`
  - Windows: `%APPDATA%/hume-sim/`

---

## Export Format

Each export includes:

- Theoretical moments table
- Correlation matrix
- Iteration snapshots (all variables over time)

---

## Development Notes

Adding / modifying equations is fairly easy. To modify one of the behavioural equations, simply find and modify the respective function in `equations.py`:

```python
def eq_production(A: float, K: float, alpha: float) -> float:
    """Y = A * K^alpha"""
    return A * (K ** alpha)
```
...and update the corespondig line in `ui/iteration_widget.py`:
```python
Y = eq_output(A, inputs["K"], params["alpha"])
```

Depending on how the equations are modified, the order of computations might need to be adapted. In the above example, A must be defined or calculated earlier, and K is the input-field value of the current iteration.

When adding new variables for a new computation, also adapt the tuples VARIABLE_KEYS and UPDATES.

There are five model parameters defined in config.toml, though only two are currently used in the functional relationships. The rest are available for extensions or experimental equations.

---

Any contributions, tests or corrections welcome.

---


