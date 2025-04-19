"""Machine‑learning / Monte‑Carlo pricing for Asian (arithmetic‑average) options."""
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from typing import Tuple
from types import SimpleNamespace


def _mc_asian_price(S0: float, K: float, T: float, r: float, sigma: float,
                    n_paths: int, m_steps: int, option_type: str) -> float:
    """Monte‑Carlo estimate of Asian option price for a single S0."""
    dt = T / m_steps
    nudt = (r - 0.5 * sigma ** 2) * dt
    sigsdt = sigma * np.sqrt(dt)

    S = np.full(n_paths, S0)
    running_sum = S.copy()
    for _ in range(m_steps):
        z = np.random.normal(size=n_paths)
        S *= np.exp(nudt + sigsdt * z)
        running_sum += S
    A = running_sum / (m_steps + 1)

    if option_type == "call":
        payoff = np.maximum(A - K, 0.0)
    else:
        payoff = np.maximum(K - A, 0.0)

    return np.exp(-r * T) * payoff.mean()


def price_asian_option_grid(params) -> Tuple[np.ndarray, np.ndarray]:
    """Return (S_grid, V_grid) using MC + polynomial Ridge regression."""
    if isinstance(params, dict):
        params = SimpleNamespace(**params)

    # Training data around strike
    S_train = np.random.uniform(0.5 * params.K, 1.5 * params.K, size=300)
    y_train = np.array([
        _mc_asian_price(S0, params.K, params.T, params.r, params.sigma,
                        params.n_paths, params.m_steps, params.option_type)
        for S0 in S_train
    ])

    model = make_pipeline(PolynomialFeatures(4), Ridge(alpha=1e-3))
    model.fit(S_train.reshape(-1, 1), y_train)

    S_grid = np.linspace(0.1 * params.K, 2.0 * params.K, params.grid_points)
    V_grid = model.predict(S_grid.reshape(-1, 1))
    V_grid = np.clip(V_grid, 0.0, None)
    return S_grid, V_grid