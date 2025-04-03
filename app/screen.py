# app/screen.py

from textual.app import ComposeResult, Screen
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static

from app.ui.iteration_widget import IterationControls
from app.ui.moments_widget import MomentsWidget
from app.ui.correlations_widget import CorrelationsWidget
from app.ui.form_widget import FormWidget


class SimScreen(Screen):
    """Main simulation screen layout."""

    def compose(self) -> ComposeResult:
        self.moments_widget = MomentsWidget(id="moments-table")
        self.corr_widget = CorrelationsWidget(id="correlations-table")
        self.form_widget = FormWidget(id="form-section")

        yield Header()
        yield Horizontal(
            Vertical(  # LEFT PANE
                Vertical(
                    self.form_widget,
                    id="form-container"
                ),
                Vertical(
                    Static("Simulation", id="sim-label", classes="title-label"),
                    IterationControls(id="sim-controls"),
                    id="button-container"
                ),
                id="left-pane"
            ),
            Vertical(  # RIGHT PANE
                Vertical(
                    Static("Theoretical Moments", id="moments-label", classes="title-label"),
                    self.moments_widget,
                    id="moments-container",
                ),
                Vertical(
                    Static("Pearson Correlation Coefficients", id="correlations-label", classes="title-label"),
                    self.corr_widget,
                    id="correlations-container"
                ),
                id="analysis-row"
            )
        )
        yield Footer()

    def on_mount(self) -> None:
        self.app.moments_widget = self.moments_widget
        self.app.corr_widget = self.corr_widget
        self.app.form_widget = self.form_widget
        self.form_widget.repopulate()



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
