"""Finite‑difference solvers for American options."""
import numpy as np
from typing import Tuple
import types


def _explicit_american_put(
    Smax: float,
    K: float,
    T: float,
    r: float,
    q: float,
    sigma: float,
    M: int,
    N: int,
):
    """Explicit (forward‑time, central‑space) scheme with early‑exercise."""
    dS = Smax / M
    dt = T / N

    # CFL‑like stability criterion
    if dt > (dS ** 2) / (sigma ** 2 * Smax ** 2):
        raise ValueError("dt too large for explicit stability; increase N or M.")

    S = np.linspace(0.0, Smax, M + 1)
    V = np.maximum(K - S, 0.0)[:, None]
    V = np.repeat(V, N + 1, axis=1)  # broadcast along time

    for n in reversed(range(N)):
        V[0, n] = K * np.exp(-r * (T - n * dt))  # left BC (S=0)
        V[-1, n] = 0.0  # right BC (S=Smax)
        for i in range(1, M):
            a = 0.5 * dt * ((sigma ** 2) * (i ** 2) - (r - q) * i)
            b = 1 - dt * ((sigma ** 2) * (i ** 2) + r)
            c = 0.5 * dt * ((sigma ** 2) * (i ** 2) + (r - q) * i)
            V[i, n] = a * V[i - 1, n + 1] + b * V[i, n + 1] + c * V[i + 1, n + 1]
        # early exercise constraint
        V[:, n] = np.maximum(V[:, n], K - S)

    return S, V[:, 0]


def _implicit_american_put(
    Smax: float,
    K: float,
    T: float,
    r: float,
    q: float,
    sigma: float,
    M: int,
    N: int,
    tol: float = 1e-8,
    max_iter: int = 5000,
):
    """Backward Euler + PSOR (Projected SOR) for Linear Complementarity."""
    dS = Smax / M
    dt = T / N

    S = np.linspace(0.0, Smax, M + 1)
    V = np.zeros((M + 1, N + 1))
    V[:, -1] = np.maximum(K - S, 0.0)

    i = np.arange(1, M)
    alpha = 0.5 * dt * ((sigma ** 2) * (i ** 2) - (r - q) * i)
    beta = 1 + dt * ((sigma ** 2) * (i ** 2) + r)
    gamma = 0.5 * dt * ((sigma ** 2) * (i ** 2) + (r - q) * i)

    a = -alpha
    b = beta
    c = -gamma
    omega = 1.2  # relaxation parameter

    for n in reversed(range(N)):
        rhs = V[1:M, n + 1].copy()
        rhs[0] -= a[0] * (K * np.exp(-r * (T - n * dt)))
        # rhs[-1] -= c[-1] * 0 (already zero)

        x = V[1:M, n + 1].copy()  # initial guess
        for _ in range(max_iter):
            x_old = x.copy()
            for j in range(M - 1):
                left = x[j - 1] if j > 0 else (K * np.exp(-r * (T - n * dt)))
                right = x[j + 1] if j < M - 2 else 0.0
                sigma_j = a[j] * left + b[j] * x[j] + c[j] * right
                x[j] = max(x[j] + omega * (rhs[j] - sigma_j) / b[j], K - S[j + 1])
            if np.linalg.norm(x - x_old, ord=np.inf) < tol:
                break

        V[1:M, n] = x
        V[0, n] = K * np.exp(-r * (T - n * dt))
        V[-1, n] = 0.0

    return S, V[:, 0]


def price_american_option_put(params) -> Tuple[np.ndarray, np.ndarray]:
    """Return grid S and option values at t=0 for provided parameters."""
    if isinstance(params, dict):
        params = types.SimpleNamespace(**params)

    Smax = params.Smax_factor * params.K

    if params.method == "explicit":
        return _explicit_american_put(
            Smax,
            params.K,
            params.T,
            params.r,
            params.q,
            params.sigma,
            params.M,
            params.N,
        )
    elif params.method == "implicit":
        return _implicit_american_put(
            Smax,
            params.K,
            params.T,
            params.r,
            params.q,
            params.sigma,
            params.M,
            params.N,
        )
    else:
        raise ValueError("Unsupported numerical method: " + params.method)