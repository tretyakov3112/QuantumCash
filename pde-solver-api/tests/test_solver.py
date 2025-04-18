"""Pytest: explicit and implicit schemes should give close results."""
import numpy as np
from types import SimpleNamespace

from solvers.american_option import _explicit_american_put, _implicit_american_put


def test_explicit_vs_implicit():
    p = SimpleNamespace(Smax_factor=3.0, K=50, T=1.0, r=0.05, q=0.0, sigma=0.2, M=80, N=500)
    S1, V1 = _explicit_american_put(p.Smax_factor * p.K, p.K, p.T, p.r, p.q, p.sigma, p.M, p.N)
    S2, V2 = _implicit_american_put(p.Smax_factor * p.K, p.K, p.T, p.r, p.q, p.sigma, p.M, p.N)
    assert np.allclose(V1, V2, atol=0.05), "Explicit and implicit solutions diverge too much"