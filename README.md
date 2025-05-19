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

![Screenshot 2025-05-01 161756](https://github.com/user-attachments/assets/1d38d79a-0510-4612-91cf-2ccee1134fe9)
![Screenshot 2025-05-02 143759](https://github.com/user-attachments/assets/b40c9b5b-2327-498d-9b2c-0240568531ea)
![Screenshot 2025-05-01 161819](https://github.com/user-attachments/assets/2df4add9-338d-4490-a7bb-7b3d1b8f9e8b)
![Screenshot 2025-05-01 161739](https://github.com/user-attachments/assets/8b1efef5-3b76-46f4-b9a3-d31779aa6d88)
![Screenshot 2025-05-01 161719](https://github.com/user-attachments/assets/232f506f-068f-4b79-93d2-8b782999efeb)
![Screenshot 2025-05-06 005803](https://github.com/user-attachments/assets/9c484a63-c8fe-4fd6-ba73-e475c1da0ad2)
