import argparse
import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

from algorithms.sorting import sort_parcels
from algorithms.knapsack import knapsack
from algorithms.dijkstra import build_graph, dijkstra, get_path, INF
from algorithms.tsp import nearest_neighbor, brute_force_tsp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BRUTE_FORCE_LIMIT = 8

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_planner(capacity=25, custom_parcels=None, custom_map=None):
    parcels = custom_parcels if custom_parcels is not None else load_json(os.path.join(BASE_DIR, "data", "parcels.json"))
    map_data = custom_map if custom_map is not None else load_json(os.path.join(BASE_DIR, "data", "locations.json"))

    warehouse = map_data["warehouse"]
    graph = build_graph(map_data["roads"])

    # Validate parcels
    dist_from_warehouse, _ = dijkstra(graph, warehouse)
    valid_parcels = []
    skipped = []
    required = ["id", "weight", "value", "priority", "deadline_hours", "location"]

    for p in parcels:
        missing = [f for f in required if f not in p]
        if missing:
            skipped.append({"id": p.get("id", "?"), "reason": f"Missing fields: {missing}"})
        elif p["weight"] <= 0 or p["value"] < 0:
            skipped.append({"id": p["id"], "reason": "Weight <= 0 or value < 0"})
        elif p["location"] not in graph:
            skipped.append({"id": p["id"], "reason": f"Location '{p['location']}' not on map"})
        elif dist_from_warehouse[p["location"]] == INF:
            skipped.append({"id": p["id"], "reason": "Unreachable from warehouse"})
        else:
            valid_parcels.append(p)

    sorted_parcels = sort_parcels(valid_parcels)
    best_value, selected, dp_table = knapsack(sorted_parcels, capacity)
    total_weight = sum(p["weight"] for p in selected)
    selected_ids = set(p["id"] for p in selected)
    unselected = [p for p in sorted_parcels if p["id"] not in selected_ids]

    parcels_at = {}
    for p in selected:
        parcels_at.setdefault(p["location"], []).append(p)
    stops = sorted(parcels_at.keys())

    # Dijkstra shortest paths
    places = [warehouse] + stops
    matrix = {}
    previous = {}
    for a in places:
        dists, prev = dijkstra(graph, a)
        matrix[a] = {b: dists[b] for b in places}
        previous[a] = prev

    warehouse_paths = {}
    for stop in stops:
        warehouse_paths[stop] = {
            "distance": matrix[warehouse][stop],
            "path": get_path(previous[warehouse], warehouse, stop)
        }

    # TSP Route
    if stops:
        nn_route, nn_distance = nearest_neighbor(matrix, warehouse, stops)
    else:
        nn_route, nn_distance = [warehouse], 0

    # Expand full road segments
    full_path = [nn_route[0]]
    for i in range(len(nn_route) - 1):
        leg = get_path(previous[nn_route[i]], nn_route[i], nn_route[i + 1])
        full_path.extend(leg[1:])

    # Exact comparison
    exact_route = None
    exact_distance = None
    if 0 < len(stops) <= BRUTE_FORCE_LIMIT:
        exact_route, exact_distance = brute_force_tsp(matrix, warehouse, stops)

    # Delivery schedule
    delivery_schedule = []
    for place in nn_route[1:-1]:
        for p in selected:
            if p["location"] == place:
                delivery_schedule.append({
                    "location": place,
                    "parcel": p
                })

    return {
        "capacity": capacity,
        "warehouse": warehouse,
        "all_locations": map_data.get("locations", list(graph.keys())),
        "roads": map_data["roads"],
        "parcels_initial": parcels,
        "parcels_sorted": sorted_parcels,
        "skipped_parcels": skipped,
        "selected_parcels": selected,
        "unselected_parcels": unselected,
        "total_weight": total_weight,
        "total_value": best_value,
        "stops": stops,
        "parcels_at_stops": {k: [p["id"] for p in v] for k, v in parcels_at.items()},
        "warehouse_paths": warehouse_paths,
        "distance_matrix": matrix,
        "matrix_places": places,
        "nn_route": nn_route,
        "nn_distance": nn_distance,
        "full_road_path": full_path,
        "exact_route": exact_route,
        "exact_distance": exact_distance,
        "delivery_schedule": delivery_schedule,
        "dp_table": dp_table
    }

class CourierHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(BASE_DIR, "web", "index.html"), "rb") as f:
                self.wfile.write(f.read())
            return

        if parsed.path == "/api/plan":
            query = urllib.parse.parse_qs(parsed.query)
            cap = int(query.get("capacity", [25])[0])
            data = run_planner(capacity=cap)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        # Serve static assets from project root
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/plan":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode("utf-8")
            payload = json.loads(body) if body else {}

            cap = int(payload.get("capacity", 25))
            custom_parcels = payload.get("parcels", None)
            custom_map = payload.get("map", None)

            data = run_planner(capacity=cap, custom_parcels=custom_parcels, custom_map=custom_map)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

def main():
    parser = argparse.ArgumentParser(description="Mini-Courier Web Server")
    parser.add_argument("--port", type=int, default=5000, help="Port to listen on (default: 5000)")
    args = parser.parse_args()

    server_address = ("127.0.0.1", args.port)
    httpd = HTTPServer(server_address, CourierHandler)
    print(f"============================================================")
    print(f"  Mini-Courier Interactive Dashboard Server")
    print(f"  Running at: http://127.0.0.1:{args.port}/")
    print(f"  Open this URL in your web browser to view the frontend!")
    print(f"============================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()
