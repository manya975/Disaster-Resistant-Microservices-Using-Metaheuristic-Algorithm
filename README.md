## 🚀 Overview

- **Problem:** When services running in a Kubernetes cluster fail or become unhealthy, we need an optimized way to reroute traffic.
- **Solution:**
  - Detect unhealthy nodes using Kubernetes Metrics API.
  - Use **ACO** to find the best rerouting path based on latency between nodes.
  - Optimize ACO parameters using a **GA microservice**.
  - All services are **Dockerized** for easy deployment.


---

## 🔧 Technologies Used

- **Python 3**
- **Flask** for the microservice API
- **Docker** for containerization
- **Kubernetes** (optional) for metric monitoring

---

## 🧠 Core Components

### 📌 1. merged.py

- Monitors CPU and memory usage via Kubernetes Metrics API.
- If metrics are zero (i.e., node failure), it triggers rerouting.
- Calls GA microservice to fetch best ACO parameters.
- Uses ACO to compute the shortest path based on latency graph.

#### 🧮 Parameters:
- `start` and `end`: Source and destination node IDs.
- `population_size`: Number of chromosomes in GA.
- `generations`: Number of generations to evolve.
- `alpha`, `beta`: ACO importance weights for pheromone and heuristic.
- `evaporation`: Rate of pheromone evaporation.
- `ants`: Number of ants used in ACO.
- `iterations`: Number of iterations of the ACO algorithm.
- Flask app that exposes:
  - `POST /test-docker`: Accepts `start`, `end`, `population_size`, and `generations`.
  - Returns: `best_parameters` (alpha, beta, evaporation, ants, iterations).

---

