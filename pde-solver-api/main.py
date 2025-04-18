from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
import numpy as np
import plotly.graph_objects as go
import uuid

from schemas import AmericanOptionInput
from solvers.american_option import price_american_option_put

app = FastAPI(title="PDE Solver API – American Option")

# -------------------------------------------------------------------
# In‑memory store for generated Plotly pages
# -------------------------------------------------------------------
PLOT_STORE: dict[str, str] = {}

# -------------------------------------------------------------------
# Root → Swagger UI, чтобы сразу открыть документацию
# -------------------------------------------------------------------
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# -------------------------------------------------------------------
# HTML endpoint: Swagger покажет HTML как текст, поэтому
# добавляем вариант, который СРАЗУ редиректит браузер на /plot/<id>
# -------------------------------------------------------------------
@app.post("/solve/american-option/view", include_in_schema=True)
async def solve_american_option_view(params: AmericanOptionInput):
    """Compute option and redirect client to a page with the interactive graph."""
    S, V0 = price_american_option_put(params)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S, y=V0, mode="lines",
                             name=f"American {params.option_type.capitalize()} t=0"))
    fig.add_vline(x=params.S0, line_dash="dash")
    fig.update_layout(title="American Option Price vs Underlying Price at t=0",
                      xaxis_title="Underlying price S",
                      yaxis_title="Option value")

    html_page = fig.to_html(full_html=True)
    plot_id = str(uuid.uuid4())
    PLOT_STORE[plot_id] = html_page

    return RedirectResponse(url=f"/plot/{plot_id}", status_code=303)

# -------------------------------------------------------------------
# GET /plot/{plot_id} – возвращает сохранённую Plotly‑страницу
# -------------------------------------------------------------------
@app.get("/plot/{plot_id}", response_class=HTMLResponse, include_in_schema=False)
async def get_plot(plot_id: str):
    html = PLOT_STORE.get(plot_id)
    if html is None:
        return HTMLResponse(content="Plot not found", status_code=404)
    return HTMLResponse(content=html)
