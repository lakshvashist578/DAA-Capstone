import argparse
import json
import os
import sys

from algorithms.sorting import sort_parcels
from algorithms.knapsack import knapsack, print_dp_table
from algorithms.dijkstra import build_graph, dijkstra, get_path, INF
from algorithms.tsp import nearest_neighbor, brute_force_tsp

VEHICLE_CAPACITY = 25
BRUTE_FORCE_LIMIT = 8

# Terminal styling helper
USE_COLOR = sys.stdout.isatty() or os.environ.get("FORCE_COLOR") == "1"

def clr(text, code):
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text

def cyan(t): return clr(t, "36")
def green(t): return clr(t, "32")
def yellow(t): return clr(t, "33")
def bold(t): return clr(t, "1")
def dim(t): return clr(t, "2")
def red(t): return clr(t, "31")
def magenta(t): return clr(t, "35")

def banner(step_num, title):
    w = 72
    line = "━" * (w - 4)
    print("\n" + cyan(f"┏{line}┓"))
    print(cyan("┃ ") + bold(f"STEP {step_num}: {title}".ljust(w - 6)) + cyan(" ┃"))
    print(cyan(f"┗{line}┛"))

def load_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(red(f"Error: file '{filename}' not found"))
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(red(f"Error: '{filename}' is not valid JSON ({e})"))
        sys.exit(1)

def check_parcels(parcels, graph, warehouse):
    dist_from_warehouse, _ = dijkstra(graph, warehouse)
    required = ["id", "weight", "value", "priority", "deadline_hours", "location"]
    valid = []
    for p in parcels:
        missing = [field for field in required if field not in p]
        if missing:
            print(yellow(f"  [!] Skipping parcel: missing fields {missing}"))
        elif p["weight"] <= 0 or p["value"] < 0:
            print(yellow(f"  [!] Skipping {p.get('id', '?')}: weight must be > 0 and value >= 0"))
        elif p["location"] not in graph:
            print(yellow(f"  [!] Skipping {p['id']}: location '{p['location']}' is not on the map"))
        elif dist_from_warehouse[p["location"]] == INF:
            print(yellow(f"  [!] Skipping {p['id']}: '{p['location']}' cannot be reached from warehouse"))
        else:
            valid.append(p)
    return valid

def prio_badge(prio):
    if prio == 1:
        return red("[P1-Urgent]")
    elif prio == 2:
        return yellow("[P2-Normal]")
    else:
        return dim("[P3-Low]")

def print_parcel_table(parcels):
    print("  ┌──────┬──────────────────┬────────┬────────┬─────────────┬──────────┬──────────────────┐")
    print("  │ " + bold(f"{'ID':<4}") + " │ " + bold(f"{'Name':<16}") + " │ " +
          bold(f"{'Wt(kg)':>6}") + " │ " + bold(f"{'Value':>6}") + " │ " +
          bold(f"{'Priority':<11}") + " │ " + bold(f"{'Deadline':>8}") + " │ " +
          bold(f"{'Destination':<16}") + " │")
    print("  ├──────┼──────────────────┼────────┼────────┼─────────────┼──────────┼──────────────────┤")
    for p in parcels:
        p_badge = prio_badge(p['priority'])
        print(f"  │ {p['id']:<4} │ {p['name']:<16} │ {p['weight']:>6} │ {p['value']:>6} │ {p_badge:<20} │ {p['deadline_hours']:>6} h │ {p['location']:<16} │")
    print("  └──────┴──────────────────┴────────┴────────┴─────────────┴──────────┴──────────────────┘")

def build_distance_matrix(graph, places):
    matrix = {}
    previous = {}
    for a in places:
        dist, prev = dijkstra(graph, a)
        matrix[a] = {b: dist[b] for b in places}
        previous[a] = prev
    return matrix, previous

def full_road_path(route, previous):
    path = [route[0]]
    for i in range(len(route) - 1):
        leg = get_path(previous[route[i]], route[i], route[i + 1])
        path.extend(leg[1:])
    return path

def progress_bar(val, max_val, length=24):
    ratio = min(1.0, val / max_val) if max_val > 0 else 0
    filled = int(round(length * ratio))
    bar = "█" * filled + "░" * (length - filled)
    pct = int(ratio * 100)
    return f"[{green(bar)}] {val}/{max_val} kg ({pct}%)"

def main():
    parser = argparse.ArgumentParser(description="NeoCourier Planner - DAA Route & Dispatch Engine")
    parser.add_argument("--parcels", default="data/parcels.json", help="Path to parcels.json")
    parser.add_argument("--locations", default="data/locations.json", help="Path to locations.json")
    parser.add_argument("--capacity", type=int, default=VEHICLE_CAPACITY, help="Vehicle capacity (kg)")
    args = parser.parse_args()

    # App Header
    print("\n" + cyan("═" * 72))
    print(bold(cyan("   📦 NEO-COURIER PLANNER  |  DAA CAPSTONE OPTIMIZATION ENGINE")))
    print(dim("   Dynamic Programming Knapsack • Dijkstra • Nearest Neighbor TSP"))
    print(cyan("═" * 72))

    banner(1, "Data Ingestion & Integrity Validation")
    parcels = load_json(args.parcels)
    map_data = load_json(args.locations)
    warehouse = map_data["warehouse"]
    graph = build_graph(map_data["roads"])

    if warehouse not in graph:
        print(red("Error: warehouse is not connected to any road"))
        sys.exit(1)
    if args.capacity < 0:
        print(red("Error: capacity cannot be negative"))
        sys.exit(1)

    print(f"  • {bold('Vehicle Capacity')}: {args.capacity} kg")
    print(f"  • {bold('Dispatch Hub')}    : {warehouse}")
    print(f"  • {bold('Network Size')}    : {len(graph)} locations, {len(map_data['roads'])} physical road links")
    print(f"  • {bold('Parcels Pool')}    : {len(parcels)} items received\n")

    parcels = check_parcels(parcels, graph, warehouse)
    if not parcels:
        print(red("No valid parcels to deliver."))
        return
    print_parcel_table(parcels)

    banner(2, "Merge Sort Ordering (Priority > Deadline)")
    sorted_parcels = sort_parcels(parcels)
    print("  Parcels arranged strictly by urgency (stable tie-breaking by deadline):\n")
    print_parcel_table(sorted_parcels)

    banner(3, "0/1 Knapsack Vehicle Loading (Dynamic Programming)")
    best_value, selected, table = knapsack(sorted_parcels, args.capacity)
    print(dim("  DP Table (Rows: parcels considered, Cols: weight limits 0..W):"))
    print_dp_table(sorted_parcels, table)

    total_weight = sum(p["weight"] for p in selected)
    print("\n  " + bold("Optimal Vehicle Loadout:"))
    print_parcel_table(selected)
    print(f"\n  • {bold('Capacity Used')}   : {progress_bar(total_weight, args.capacity)}")
    print(f"  • {bold('Total Revenue')}   : {green('₹' + str(best_value))}")

    left_behind = [p for p in sorted_parcels if p not in selected]
    deferred = ", ".join(p["id"] for p in left_behind) if left_behind else "None (All loaded!)"
    print(f"  • {bold('Queued Next Trip')}: {yellow(deferred)}")

    if not selected:
        print(yellow("\nNo parcel fits in the vehicle within specified capacity."))
        return

    banner(4, "Grouping Stops from Manifest")
    parcels_at = {}
    for p in selected:
        parcels_at.setdefault(p["location"], []).append(p["id"])
    stops = sorted(parcels_at.keys())
    for place in stops:
        items = ", ".join(parcels_at[place])
        print(f"  📍 {bold(place):<20} ➔ {items}")

    banner(5, "Dijkstra Shortest Paths Across Road Network")
    dist, prev = dijkstra(graph, warehouse)
    for place in stops:
        path = get_path(prev, warehouse, place)
        route_str = " ➔ ".join(path)
        print(f"  {warehouse} ➔ {bold(place):<18} : {dist[place]:>3} km  {dim('(' + route_str + ')')}")

    places = [warehouse] + stops
    matrix, previous = build_distance_matrix(graph, places)
    print("\n  " + bold("Shortest Metric Distance Matrix (km):"))
    short = lambda name: name[:9]
    print(f"  {'':<11}" + "".join(f"{short(b):>11}" for b in places))
    for a in places:
        row_str = f"  {short(a):<11}"
        for b in places:
            d = matrix[a][b]
            row_str += f"{dim('·') if a == b else str(d):>11}"
        print(row_str)

    banner(6, "Nearest Neighbor TSP Tour Construction")
    route, total_distance = nearest_neighbor(matrix, warehouse, stops)
    route_display = " ➔ ".join(bold(s) for s in route)
    print(f"  Stop Order Tour:\n  {route_display}\n")

    banner(7, "Final Optimized Dispatch Plan")
    actual_path = full_road_path(route, previous)
    print("  " + bold("Turn-by-turn road route:"))
    print("  " + green(" ➔ ".join(actual_path)))

    print("\n  ╭────────────────────────────────────────────────────────────────╮")
    print(f"  │  {bold('Total Tour Distance')} : {cyan(str(total_distance) + ' km')} (round-trip back to {warehouse})")
    print(f"  │  {bold('Parcels Delivered')}   : {len(selected)} items ({', '.join(p['id'] for p in selected)})")
    print(f"  │  {bold('Payload Carried')}    : {total_weight} kg / {args.capacity} kg capacity")
    print(f"  │  {bold('Total Value Earned')} : {green('₹' + str(best_value))}")
    print("  ╰────────────────────────────────────────────────────────────────╯")

    print("\n  " + bold("Delivery Schedule & Deadlines:"))
    for place in route[1:-1]:
        for p in selected:
            if p["location"] == place:
                print(f"    • {place:<18} {bold(p['id'])} {p['name']:<15} {prio_badge(p['priority'])} (Deadline: {p['deadline_hours']}h)")

    print("\n  " + bold("Algorithmic Verification (Nearest Neighbor vs Brute Force):"))
    if len(stops) <= BRUTE_FORCE_LIMIT:
        best_route, best_total = brute_force_tsp(matrix, warehouse, stops)
        print(f"    • Exact Optimal Route (Brute Force $O(n!)$) : {green(str(best_total) + ' km')}")
        print(f"    • Nearest Neighbor Heuristic ($O(n^2)$)        : {cyan(str(total_distance) + ' km')}")
        diff = total_distance - best_total
        print(f"    • Heuristic Approximation Gap                 : {yellow('+' + str(diff) + ' km')}")
    else:
        print(f"    (Exact comparison skipped because stops > {BRUTE_FORCE_LIMIT})")

    print("\n" + cyan("━" * 72) + "\n")

if __name__ == "__main__":
    main()
