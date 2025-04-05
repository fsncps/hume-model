from textual.widgets import Static, Input
from textual.containers import Horizontal, Vertical
from textual.widget import Widget

from app.config_loader import load_config

# Hardcoded fallback defaults
FALLBACK_DEFAULTS = {
    "defaults": {
        "Y": 1.0, "C": 0.6, "I": 0.4, "K": 5.0, "r": 0.03, "s": 0.2, "p": 0.05,
        "theta": 0.5, "M": 1.0, "P": 1.0, "pi": 0.0, "K_last": 5.0, "P_last": 1.0,
    },
    "parameters": {
        "alpha": 0.33, "beta": 0.96, "delta": 0.05, "gamma": 0.004, "sigma": 1.0,
    },
    "shocks": {
        "A-mean": 1.0, "A-stderr": 0.01,
        "D-mean": 1.0, "D-stderr": 0.02,
    },
}

# Metadata only — not actual values
VARIABLES = [
    ("Y",      "Output Y",                " = A⋅Kᵅ"),
    ("C",      "Consumption C",           " = (1−s) ⋅ Y ⋅ D"),
    ("I",      "Investment I",            " = s ⋅ Y ⋅ D"),
    ("K",      "Capital Stock K",         " = (1−δ) ⋅ K₋₁+I"),
    ("r",      "Interest Rate r",         " = p − γ"),
    ("s",      "Saving Rate s",           " = C/Y"),
    ("p",      "Profit Rate p",           " = α ⋅ Y/K"),
    ("theta",  "Wealth Concentration θ",  " = K/M"),
    ("P",      "Price Level P",           " = M/Y"),
    ("pi",     "Inflation π",             " = P/P₋₁ − 1"),
    ("M",      "Money Supply M",          " (assumed fixed)"),
    ("K_last", "Lagged K",                " (K₋₁)"),
    ("P_last", "Lagged P",                " (P₋₁)"),
]

PARAMETERS = [
    ("alpha", "Output Elasticity α"),
    ("beta", "Discout Factor β"),
    ("delta", "Depreciation Rate δ"),
    ("gamma", "Min. Profit Rate γ"),
    ("sigma", "Consumption Elasticity σ"),
]

SHOCKS = [
    ("A", "Labour Shock A"),
    ("D", "Demand Shock D"),
]


class FormWidget(Vertical):
    def compose(self):
        yield Static("Initial Values", id="init-label", classes="title-label")
        yield Vertical(
            *[
                Horizontal(
                    Static(f"{label}:", classes="field-label"),
                    Input(id=f"init-{var}", classes="field-input"),
                    Static(equation, classes="equation-label"),
                    classes="field-row"
                )
                for var, label, equation in VARIABLES
            ],
            id="init-values"
        )

        yield Static("Parameters", id="param-label", classes="title-label")
        yield Vertical(
            *[
                Horizontal(
                    Static(label + ":", classes="field-label"),
                    Input(id=f"param-{name}", classes="field-input"),
                    classes="field-row"
                )
                for name, label in PARAMETERS
            ],
            id="param-values"
        )

        yield Static("Shocks (mean, stderr)", id="shock-label", classes="title-label")
        yield Vertical(
            *[
                Horizontal(
                    Static(label + ":", classes="field-label"),
                    Input(id=f"shock-{name}-mean", classes="field-input"),
                    Input(id=f"shock-{name}-stderr", classes="field-input"),
                    classes="field-row"
                )
                for name, label in SHOCKS
            ],
            id="shock-values"
        )

    def repopulate(self):
        try:
            config = load_config()
        except Exception:
            config = {}

        defaults = config.get("defaults", FALLBACK_DEFAULTS["defaults"])
        params = config.get("parameters", FALLBACK_DEFAULTS["parameters"])
        shocks = config.get("shocks", FALLBACK_DEFAULTS["shocks"])

        for var, _, _ in VARIABLES:
            value = defaults.get(var, FALLBACK_DEFAULTS["defaults"].get(var, ""))
            self.query_one(f"#init-{var}", Input).value = str(value)

        for name, _ in PARAMETERS:
            value = params.get(name, FALLBACK_DEFAULTS["parameters"].get(name, ""))
            self.query_one(f"#param-{name}", Input).value = str(value)

        for name, _ in SHOCKS:
            mean_key = f"{name}-mean"
            stderr_key = f"{name}-stderr"
            mean = shocks.get(mean_key, FALLBACK_DEFAULTS["shocks"].get(mean_key, ""))
            stderr = shocks.get(stderr_key, FALLBACK_DEFAULTS["shocks"].get(stderr_key, ""))
            self.query_one(f"#shock-{name}-mean", Input).value = str(mean)
            self.query_one(f"#shock-{name}-stderr", Input).value = str(stderr)

