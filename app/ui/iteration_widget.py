from textual.widgets import Button, Static, Input
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.widget import Widget
from textual.reactive import reactive
import random

from ..equations import *
from app.utils.exporter import export_simulation  # ✅ new import

VARIABLE_KEYS = [
    "Y", "C", "I", "K", "r", "s", "p", "theta", "M", "P", "pi", "K_last", "P_last"
]
PARAMETER_KEYS = ["alpha", "beta", "delta", "gamma", "sigma"]
SHOCK_KEYS = ["A-mean", "A-stderr", "D-mean", "D-stderr"]

class NewIteration(Message):
    def __init__(self, sender: Widget, data: dict) -> None:
        super().__init__()
        self.sender = sender
        self.data = data


class IterationControls(Vertical):
    counter = reactive(0)
    simulation_state = reactive(list)

    def compose(self):

        yield Horizontal(
            Button("Iterate", id="iterate-button"),
            Button("Clear", id="clear-button"),
            Button("Export", id="export-button"),
            id="button-row"
        )

        yield Static(f"Iterations: {self.counter}", id="iteration-counter")


    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "iterate-button":
            self.do_iteration()
            self.app.log(f"[IterationControls] Iterating with {len(self.simulation_state)} steps")

            if self.simulation_state:
                self.app.moments_widget.update_from_simulation(self.simulation_state)
                self.app.corr_widget.update_from_simulation(self.simulation_state)

        elif event.button.id == "clear-button":
            self.app.log("[IterationControls] Clearing simulation...")
            self.simulation_state = []
            self.counter = 0
            self.query_one("#iteration-counter", Static).update(f"Iterations: {self.counter}")
            self.app.form_widget.repopulate()
            self.app.moments_widget.update_from_simulation([])
            self.app.corr_widget.update_from_simulation([])

        elif event.button.id == "export-button":
            self.app.log("[Export] Saving...")
            moments = self.app.moments_widget.get_data_as_dicts()
            correlations = self.app.corr_widget.get_data_as_matrix()
            path = export_simulation(moments, correlations, self.simulation_state)
            self.app.notify(f"Export saved to: {path}")
            self.app.log(f"[Export] Done → {path}")


    def do_iteration(self):
        def get(var: str) -> float:
            try:
                return float(self.screen.query_one(f"#init-{var}", Input).value)
            except Exception:
                try:
                    return float(self.screen.query_one(f"#param-{var}", Input).value)
                except Exception:
                    try:
                        return float(self.screen.query_one(f"#shock-{var}", Input).value)
                    except Exception as e:
                        raise ValueError(f"Failed to get value for '{var}': {e}")

        inputs = {key: get(key) for key in VARIABLE_KEYS}
        params = {key: get(key) for key in PARAMETER_KEYS}
        shocks = {key: get(key) for key in SHOCK_KEYS}

        A = random.gauss(shocks["A-mean"], shocks["A-stderr"])
        D = random.gauss(shocks["D-mean"], shocks["D-stderr"])
        self.app.log(f"[do_iteration] Sampled A={A:.5f}, D={D:.5f}")

        Y = eq_output(A, inputs["K"], params["alpha"])
        C = eq_consumption(Y, inputs["s"], D)
        I = eq_investment(Y, inputs["s"], D)
        K_new = eq_capital_accumulation(inputs["K_last"], I, params["delta"])
        p = eq_profit(params["alpha"], Y, K_new)
        r = eq_interest_rate(p, params["gamma"])
        s_new = eq_savings_rate(C, Y)
        theta = eq_wealth_concentration(K_new, inputs["M"])
        P = eq_price_level(inputs["M"], Y)
        pi = eq_inflation(P, inputs["P_last"])

        updates = {
            "Y": Y,
            "C": C,
            "I": I,
            "K": K_new,
            "p": p,
            "r": r,
            "s": s_new,
            "theta": theta,
            "P": P,
            "pi": pi,
            "K_last": K_new,
            "P_last": P,
        }

        for key, val in updates.items():
            widget = self.screen.query_one(f"#init-{key}", Input)
            widget.value = f"{val:.5f}"

        self.simulation_state.append({k: float(f"{v:.5f}") for k, v in updates.items()})
        self.counter += 1
        self.query_one("#iteration-counter", Static).update(f"Iterations: {self.counter}")
        self.post_message(NewIteration(self, updates))

        self.app.log(f"Simulation State [{self.counter} iterations]:")
        for i, row in enumerate(self.simulation_state, 1):
            self.app.log(f"{i}: {row}")

        self.app.moments_widget.update_from_simulation(self.simulation_state)
        self.app.corr_widget.update_from_simulation(self.simulation_state)


# EQUATION_MARKDOWN = """
# ### Modellgleichungen
#
# | Beschreibung              | Gleichung                            |
# |---------------------------|---------------------------------------|
# | Produktion Y              | `Y = A * K^alpha`                    |
# | Konsum C                  | `C = (1 - s) * Y * D`                |
# | Investition I             | `I = s * Y * D`                      |
# | Gesamtnachfrage Y         | `Y = C + I`                          |
# | Kapital K                 | `K = (1 - delta) * K(-1) + I`        |
# | Profit p                  | `p = alpha * Y / K`                  |
# | Zins r                    | `r = p - gamma`                      |
# | Sparrate s                | `s = C / Y`                          |
# | Kreditangebot K           | `K = s * Y`                          |
# | Vermögenskonz. θ          | `θ = K / M`                          |
# | Geldmenge M               | `M = ... (exogen)`                  |
# | Preisniveau P             | `P = M / Y`                          |
# | Inflation π               | `π = P / P(-1) - 1`                  |
# | Arbeit A                  | `A = ... (exogen)`                  |
# | Nachfrage D               | `D = ... (exogen)`                  |
# """
#
#
