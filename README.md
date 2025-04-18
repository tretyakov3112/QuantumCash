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

![alt text](https://github.com/tretyakov3112/QuantumCash/tree/main/pde-solver-api/default_params.png?raw=true)
Here you can see graph with default params used. Feel free to adjust them so you can get different results. It is possible to run several graphs on the same server because they will have different ids.