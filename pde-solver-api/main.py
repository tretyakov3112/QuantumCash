"""FastAPI entrypoint for QuantumCash PDE Solver API.
Provides endpoints to price options and serve Plotly charts.
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import numpy as np
import plotly.graph_objects as go
import uuid

from schemas import AmericanOptionInput, AsianOptionInput
from solvers.american_option import price_american_option_put
from solvers.asian_option_ml import price_asian_option_grid

app = FastAPI(title="QuantumCash PDE Solver API")

# In‑memory store for generated plots {plot_id: html_string}
PLOT_STORE = {}

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _store_plot(fig) -> str:
    """Save Plotly fig HTML in global store and return its UUID id."""
    plot_id = str(uuid.uuid4())
    PLOT_STORE[plot_id] = fig.to_html(full_html=True)
    # log to console for convenience
    print(f"Plot ready: /plot/{plot_id}")
    return plot_id


def _open_tab_html(url: str) -> str:
    """Return HTML page that opens *url* in a new tab and then returns Swagger docs."""
    return f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8'>
    <title>Opening plot...</title>
    <script type='text/javascript'>
      window.open('{url}', '_blank');
      window.location.href = '/docs';
    </script>
  </head>
  <body>
    Plot is opening in a new tab… <br/>
    <a href='{url}' target='_blank'>Open manually</a>
  </body>
</html>
"""

# ---------------------------------------------------------------------------
# Endpoints: American option
# ---------------------------------------------------------------------------

@app.post("/solve/american-option/json")
async def solve_american_json(params: AmericanOptionInput):
    S, V = price_american_option_put(params)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S, y=V, mode="lines", name="American option"))
    fig.update_layout(title="American Option Price vs S0",
                      xaxis_title="Underlying price S",
                      yaxis_title="Option value")
    plot_id = _store_plot(fig)
    return JSONResponse({
        "S_grid": S.tolist(),
        "V_grid": V.tolist(),
        "plot_id": plot_id,
        "plot_url": f"/plot/{plot_id}"
    })

@app.post("/solve/american-option/view", response_class=HTMLResponse)
async def solve_american_view(params: AmericanOptionInput):
    S, V = price_american_option_put(params)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S, y=V, mode="lines", name="American option"))
    fig.update_layout(title="American Option Price vs S0",
                      xaxis_title="Underlying price S",
                      yaxis_title="Option value")
    plot_id = _store_plot(fig)
    return HTMLResponse(content=_open_tab_html(f"/plot/{plot_id}"))

# ---------------------------------------------------------------------------
# Endpoints: Asian option (ML)
# ---------------------------------------------------------------------------

@app.post("/solve/asian-option/json")
async def solve_asian_json(params: AsianOptionInput):
    S, V = price_asian_option_grid(params)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S, y=V, mode="lines", name="Asian option"))
    fig.update_layout(title="Asian Option Price vs S0",
                      xaxis_title="Underlying price S",
                      yaxis_title="Option value")
    plot_id = _store_plot(fig)
    return JSONResponse({
        "S_grid": S.tolist(),
        "V_grid": V.tolist(),
        "plot_id": plot_id,
        "plot_url": f"/plot/{plot_id}"
    })

@app.post("/solve/asian-option/view", response_class=HTMLResponse)
async def solve_asian_view(params: AsianOptionInput):
    S, V = price_asian_option_grid(params)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S, y=V, mode="lines", name="Asian option"))
    fig.update_layout(title="Asian Option Price vs S0",
                      xaxis_title="Underlying price S",
                      yaxis_title="Option value")
    plot_id = _store_plot(fig)
    return HTMLResponse(content=_open_tab_html(f"/plot/{plot_id}"))

# ---------------------------------------------------------------------------
# Retrieve stored Plotly chart
# ---------------------------------------------------------------------------

@app.get("/plot/{plot_id}", response_class=HTMLResponse)
async def get_plot(plot_id: str):
    html = PLOT_STORE.get(plot_id)
    if html is None:
        return HTMLResponse("Plot not found", status_code=404)
    return HTMLResponse(content=html)

# ---------------------------------------------------------------------------
# Root – redirect to docs
# ---------------------------------------------------------------------------

@app.get("/", include_in_schema=False)
async def root():
    return HTMLResponse("<script>window.location.href='/docs';</script>")