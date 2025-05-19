# import requests
# import os
# import numpy as np

# # Kubernetes Metrics API URL or endpoint
# K8S_METRICS_URL = os.getenv("K8S_METRICS_URL", "http://localhost:9999/apis/metrics.k8s.io/v1beta1/nodes")

# # Your latency graph data
# NUM_NODES = 6
# latency_graph = np.array([
#     [0, 2, 0, 1, 0, 0],
#     [2, 0, 3, 2, 0, 0],
#     [0, 3, 0, 0, 7, 3],
#     [1, 2, 0, 0, 4, 0],
#     [0, 0, 7, 4, 0, 1],
#     [0, 0, 3, 0, 1, 0]
# ])

# def heuristic(i, j):
#     return 1 / latency_graph[i][j] if latency_graph[i][j] > 0 else 0

# def run_aco(start, end, alpha, beta, evaporation, ants, iterations):
#     pheromone = np.ones_like(latency_graph) * 0.1
#     best_path = None
#     best_cost = float('inf')

#     for _ in range(iterations):
#         all_paths = []
#         all_costs = []

#         for _ in range(ants):
#             current = start
#             visited = [current]
#             cost = 0

#             while current != end:
#                 probabilities = []
#                 for j in range(NUM_NODES):
#                     if j not in visited and latency_graph[current][j] > 0:
#                         tau = pheromone[current][j] ** alpha
#                         eta = heuristic(current, j) ** beta
#                         probabilities.append(tau * eta)
#                     else:
#                         probabilities.append(0)

#                 total = sum(probabilities)
#                 if total == 0:
#                     break

#                 probabilities = [p / total for p in probabilities]
#                 next_node = np.random.choice(len(probabilities), p=probabilities)
#                 visited.append(next_node)
#                 cost += latency_graph[current][next_node]
#                 current = next_node

#             if visited[-1] == end:
#                 all_paths.append(visited)
#                 all_costs.append(cost)
#                 if cost < best_cost:
#                     best_cost = cost
#                     best_path = visited

#         pheromone *= (1 - evaporation)
#         for path, cost in zip(all_paths, all_costs):
#             for i in range(len(path) - 1):
#                 a, b = path[i], path[i + 1]
#                 pheromone[a][b] += 100 / cost
#                 pheromone[b][a] += 100 / cost

#     return best_path, best_cost

# def fetch_parameters_from_microservice(start, end, population_size=10, generations=10):
#     url = "http://localhost:9999/test-docker"
#     params = {
#         "start": start,
#         "end": end,
#         "population_size": population_size,
#         "generations": generations
#     }

#     try:
#         response = requests.get(url, params=params, timeout=5)
#         response.raise_for_status()

#         data = response.json()
#         if "best_parameters" not in data:
#             print("Error: 'best_parameters' not found in response.")
#             return None
#         return data["best_parameters"]

#     except requests.RequestException as e:
#         print(f"Error contacting optimization microservice: {e}")
#         return None
#     except ValueError:
#         print("Error: Failed to parse the response as JSON.")
#         return None

# def get_default_parameters():
#     return {
#         "alpha": 1.0,
#         "beta": 2.0,
#         "evaporation": 0.5,
#         "ants": 10,
#         "iterations": 50
#     }

# def get_k8s_metrics():
#     try:
#         response = requests.get(K8S_METRICS_URL, timeout=5)
#         response.raise_for_status()

#         data = response.json()

#         cpu_usage = 0
#         memory_usage = 0
#         for node in data["items"]:
#             cpu_usage += int(node['usage']['cpu'].replace('n', ''))
#             memory_usage += int(node['usage']['memory'].replace('Ki', '').replace('Mi', ''))

#         return cpu_usage, memory_usage

#     except requests.RequestException as e:
#         print(f"Error contacting Kubernetes Metrics API: {e}")
#         return None, None

# def check_service_health(cpu_usage, memory_usage):
#     if cpu_usage == 0 or memory_usage == 0:
#         print("Warning: Service has crashed! CPU or Memory usage is 0.")
#         return False
#     return True

# def reroute_service(start, end, params):
#     print("Rerouting service to the best path...")
#     best_path, total_latency = run_aco(
#         start,
#         end,
#         alpha=params["alpha"],
#         beta=params["beta"],
#         evaporation=params["evaporation"],
#         ants=params["ants"],
#         iterations=params["iterations"]
#     )
#     print(f"Best Path: {best_path}")
#     print(f"Total Latency: {total_latency}")
#     # Here you would implement the actual rerouting logic to the best path.
#     return best_path

# def run_combined():
#     print("Checking service health...")

#     cpu_usage, memory_usage = get_k8s_metrics()

#     if cpu_usage is None or memory_usage is None:
#         print("Error: Failed to fetch Kubernetes metrics.")
#         return

#     if not check_service_health(cpu_usage, memory_usage):
#         print("Service is down! Rerouting service to best path...")
        
#         # Reroute service if failure occurs
#         start = 0
#         end = 5
#         population_size = 10
#         generations = 10
#         print("\nFetching best parameters from microservice...")
#         params = fetch_parameters_from_microservice(start, end, population_size, generations)

#         if not params:
#             print("Failed to fetch parameters from microservice. Using default parameters instead.")
#             params = get_default_parameters()
#             print("Using default parameters:", params)
#         else:
#             print("Using parameters from microservice:", params)

#         rerouted_path = reroute_service(start, end, params)
#         print("Service has been rerouted to:", rerouted_path)
        
#     else:
#         print(f"Service is healthy. CPU Usage: {cpu_usage}, Memory Usage: {memory_usage}")

# if __name__ == "__main__":
#     run_combined() 
import requests
import os
import numpy as np

K8S_METRICS_URL = os.getenv("K8S_METRICS_URL", "http://localhost:9999/apis/metrics.k8s.io/v1beta1/nodes")

NUM_NODES = 6
latency_graph = np.array([
    [0, 2, 0, 1, 0, 0],
    [2, 0, 3, 2, 0, 0],
    [0, 3, 0, 0, 7, 3],
    [1, 2, 0, 0, 4, 0],
    [0, 0, 7, 4, 0, 1],
    [0, 0, 3, 0, 1, 0]
])

def heuristic(i, j):
    return 1 / latency_graph[i][j] if latency_graph[i][j] > 0 else 0

def run_aco(start, end, alpha, beta, evaporation, ants, iterations):
    pheromone = np.ones_like(latency_graph) * 0.1
    best_path = None
    best_cost = float('inf')

    for _ in range(iterations):
        all_paths = []
        all_costs = []

        for _ in range(ants):
            current = start
            visited = [current]
            cost = 0

            while current != end:
                probabilities = []
                for j in range(NUM_NODES):
                    if j not in visited and latency_graph[current][j] > 0:
                        tau = pheromone[current][j] ** alpha
                        eta = heuristic(current, j) ** beta
                        probabilities.append(tau * eta)
                    else:
                        probabilities.append(0)

                total = sum(probabilities)
                if total == 0:
                    break

                probabilities = [p / total for p in probabilities]
                next_node = np.random.choice(len(probabilities), p=probabilities)
                visited.append(next_node)
                cost += latency_graph[current][next_node]
                current = next_node

            if visited[-1] == end:
                all_paths.append(visited)
                all_costs.append(cost)
                if cost < best_cost:
                    best_cost = cost
                    best_path = visited

        pheromone *= (1 - evaporation)
        for path, cost in zip(all_paths, all_costs):
            for i in range(len(path) - 1):
                a, b = path[i], path[i + 1]
                pheromone[a][b] += 100 / cost
                pheromone[b][a] += 100 / cost

    return best_path, best_cost

def fetch_parameters_from_microservice(start, end, population_size=10, generations=10):
    url = "http://localhost:9999/test-docker"
    payload = {
        "start": start,
        "end": end,
        "population_size": population_size,
        "generations": generations
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "best_parameters" not in data:
            print("Error: 'best_parameters' not found in response.")
            return None
        return data["best_parameters"]

    except requests.RequestException as e:
        return None
    except ValueError:
        print("Error: Failed to parse the response as JSON.")
        return None

def parse_cpu(cpu_str):
    if cpu_str.endswith("n"):
        return float(cpu_str[:-1]) / 1e9  
    elif cpu_str.endswith("u"):
        return float(cpu_str[:-1]) / 1e6 
    elif cpu_str.endswith("m"):
        return float(cpu_str[:-1]) / 1000 
    else:
        return float(cpu_str)

def parse_memory(mem_str):
    if mem_str.endswith("Ki"):
        return float(mem_str[:-2]) / 1024 
    elif mem_str.endswith("Mi"):
        return float(mem_str[:-2])
    elif mem_str.endswith("Gi"):
        return float(mem_str[:-2]) * 1024  
    elif mem_str.endswith("Ti"):
        return float(mem_str[:-2]) * 1024 * 1024 
    else:
        return float(mem_str) / (1024 * 1024) 

def fetch_cpu_and_memory_usage():
    try:
        response = requests.get(K8S_METRICS_URL, timeout=5)
        response.raise_for_status()
        metrics = response.json()

        cpu_usage = 0.0
        memory_usage = 0.0
        for node in metrics["items"]:
            cpu_usage += parse_cpu(node["usage"]["cpu"])
            memory_usage += parse_memory(node["usage"]["memory"])

        #return cpu_usage, memory_usage
        return 0,0

    except requests.RequestException as e:
        return 0, 0
    except ValueError:
        print("Error: Failed to parse the metrics response as JSON.")
        return 0, 0

def reroute_service(start, end, params):
    print("Rerouting service to the best path...")
    best_path, total_latency = run_aco(
        start,
        end,
        alpha=params["alpha"],
        beta=params["beta"],
        evaporation=params["evaporation"],
        ants=params["ants"],
        iterations=params["iterations"]
    )
    print(f"Best Path: {best_path}")
    print(f"Total Latency: {total_latency}")
    return best_path

def run_combined():
    print("Checking service health...")

    cpu_usage, memory_usage = fetch_cpu_and_memory_usage()
    print(f"CPU Usage: {cpu_usage:.3f} cores, Memory Usage: {memory_usage:.2f} Mi")

    if cpu_usage == 0 and memory_usage == 0:
        print("Service is DOWN (CPU=0 and Memory=0). Rerouting required!")

        start, end = 0, 5

        print("\nFetching best parameters from microservice...")
        params = fetch_parameters_from_microservice(start, end)

        if not params:
            print("Fallback to default parameters.")
            params = {"alpha": 1.2, "beta": 2.5, "evaporation": 0.3, "ants": 10, "iterations": 50}

        rerouted_path = reroute_service(start, end, params)
        print("Service rerouted to path:", rerouted_path)
    else:
        print("Service is healthy.")

if __name__ == "__main__":
    run_combined()
