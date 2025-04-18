# QuantumCash
Quantum ML trading bot
This repository contains a FastAPI micro‑service that prices American (put/call) options with explicit or implicit finite‑difference schemes and returns an interactive Plotly chart.

---
## Installation

> **Prerequisite**: [Mamba](https://mamba.readthedocs.io/) (or Conda) 

Clone the repo and install the dependencies:

```bash
mamba install -y --file requirements.txt
```
### To start server in bash use
```bash
cd pde-solver-api
uvicorn main:app --reload
```

Then follow the IP adress (opens in browser) and then click ```try out``` button at ```/solve/american-option/view```. If you want, you can change params of calculations. After changing them you can press big blue button ```execute```. In your console (where server was started) will be displayed info in format ```GET /plot/{id} HTTP/1.1". Copy "plot/{id}``` and insert link in your browser: ```127.0.0.1:8000/plot/{id}``` so you will see graph of calculations.

![plot](pde-solver-api/default_params.png?raw=true)
Here you can see graph with default params used. Feel free to adjust them so you can get different results. It is possible to run several graphs on the same server because they will have different ids.

### Contributed

Tretiakov Aleksandr (group 206), Churilkin Artem(group 206), Nikiforov Dmitrii(group 205).

### Zone of responsibility

Tretiakov Aleksandr - idea founder, Quantum ML-engineer, financial analyst and explicit scheme creator

Churilkin Artem - tech lead, ML-engineer, api-manager  

Nikiforov Dmitrii - financial consultant, code reviewer, implicit scheme creator, Genius, Billionaire, Playboy, Philanthropist

### Conclusions

QuantumCash demonstrates how classical numerical methods for PDEs can be seamlessly integrated into a modern, cloud-ready API architecture. The project provides:

- A robust backend for pricing American-style options using both explicit and implicit finite-difference methods.
- An interactive Plotly-based frontend for instant visualization of results.
- A clean FastAPI interface suitable for integration into trading systems, research pipelines, or quantum simulation frameworks.

The modular design allows for rapid extension — whether incorporating new asset models (e.g., stochastic volatility, jumps), integrating quantum solvers, or scaling up with GPU/cloud infrastructure.

This foundation bridges traditional computational finance with modern software engineering practices, making it a practical toolkit for research, prototyping, and beyond.
