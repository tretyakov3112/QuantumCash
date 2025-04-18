from pydantic import BaseModel, Field
from typing import Literal


class AmericanOptionInput(BaseModel):
    """Input data for pricing an American option (put/call)."""

    sigma: float = Field(..., gt=0, description="Volatility of the underlying")
    S0: float = Field(..., gt=0, description="Current underlying price")
    K: float = Field(..., gt=0, description="Strike price")
    T: float = Field(..., gt=0, description="Time to maturity (years)")
    r: float = Field(..., description="Risk‑free rate")
    q: float = Field(0.0, description="Continuous dividend yield")
    Smax_factor: float = Field(3.0, gt=1, description="Upper grid bound as multiple of K")
    M: int = Field(200, gt=10, description="Number of spatial steps")
    N: int = Field(1000, gt=10, description="Number of time steps")
    method: Literal["explicit", "implicit"] = Field(
        "implicit", description="Numerical scheme to use"
    )
    option_type: Literal["put", "call"] = Field(
        "put", description="American option type. Only 'put' supported currently."
    )