"""
Question 2 - Part 1: Link-State Routing (Dijkstra's Algorithm)
Network topology:
    0 --1-- 1
    |  \    |
    7   3   1
    |    \  |
    3 --2-- 2
"""

import heapq

#  Network representation (adjacency list with link costs) 
network_graph = {
    0: {1: 1, 2: 3, 3: 7},
    1: {0: 1, 2: 1},
    2: {0: 3, 1: 1, 3: 2},
    3: {0: 7, 2: 2},
}

ALL_NODES = list(network_graph.keys())
INFINITY  = float('inf')


def run_dijkstra(source_node):
    """
    Execute Dijkstra's shortest path algorithm from the given source node.
    
    Args:
        source_node: The starting node for shortest path computation
    
    Returns:
        distances: Dictionary mapping each destination to its minimum cost from source
        first_hop: Dictionary mapping each destination to the first hop neighbor on the shortest path
    """
    # Initialize distance to all nodes as infinity, except source node itself
    distances = {node: INFINITY for node in ALL_NODES}
    first_hop = {node: None for node in ALL_NODES}
    distances[source_node] = 0

    # Priority queue stores (cumulative_cost, current_node)
    priority_queue = [(0, source_node)]

    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)
        
        # Skip stale entries where we already found a better path
        if current_cost > distances[current_node]:
            continue
            
        # Examine all neighbors of the current node
        for neighbor, link_cost in network_graph[current_node].items():
            alternative_path_cost = distances[current_node] + link_cost
            
            # If we found a shorter path to the neighbor, update and propagate
            if alternative_path_cost < distances[neighbor]:
                distances[neighbor] = alternative_path_cost
                # Determine the first hop: if source is direct neighbor, use neighbor; otherwise inherit
                first_hop[neighbor] = neighbor if current_node == source_node else first_hop[current_node]
                heapq.heappush(priority_queue, (alternative_path_cost, neighbor))

    return distances, first_hop


def display_routing_table(source_node, distances, first_hop):
    """Pretty-print the cost vector and routing table for a single source node."""
    print(f"\n{'='*50}")
    print(f"  Node {source_node} — Dijkstra's Algorithm Results")
    print(f"{'='*50}")

    # Display cost vector (shortest path distances to all destinations)
    print(f"\n  Cost vector (shortest distances from Node {source_node}):")
    print(f"  {'Destination':<15} {'Cost':<10} {'Next Hop'}")
    print(f"  {'-'*38}")
    for destination in ALL_NODES:
        if destination == source_node:
            continue
        next_hop_node = first_hop[destination]
        path_cost = distances[destination]
        print(f"  {destination:<15} {path_cost:<10} {next_hop_node}")

    # Display complete routing table
    print(f"\n  Routing Table at Node {source_node}:")
    print(f"  {'Destination':<15} {'Next Hop':<12} {'Total Cost'}")
    print(f"  {'-'*40}")
    for destination in ALL_NODES:
        if destination == source_node:
            continue
        print(f"  {destination:<15} {first_hop[destination]:<12} {distances[destination]}")


#  Execute Dijkstra's algorithm from every node in the network 
print("\n" + "="*50)
print("  PART 1: LINK-STATE ROUTING (DIJKSTRA'S ALGORITHM)")
print("="*50)

for source_node in ALL_NODES:
    shortest_distances, next_hop_table = run_dijkstra(source_node)
    display_routing_table(source_node, shortest_distances, next_hop_table)

print("\n" + "="*50 + "\n")