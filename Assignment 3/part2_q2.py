"""
Question 2 - Part 2: Distance-Vector Routing (Bellman-Ford)
Implements: initialize_routing_table0..3() and update_routing_table0..3()
Network topology:
    0 --1-- 1
    |  \    |
    7   3   1
    |    \  |
    3 --2-- 2
"""

INFINITY = float('inf')

#  Direct link costs between neighboring nodes (INFINITY = not directly connected) 
LINK_COSTS = [
    [0,   1,   3,   7  ],   # from node 0
    [1,   0,   1,   INFINITY],   # from node 1
    [3,   1,   0,   2  ],   # from node 2
    [7,   INFINITY, 2,   0  ],   # from node 3
]

#  Distance tables: routing_table[node][destination][via_neighbor] = cost 
routing_table = [[[ INFINITY]*4 for _ in range(4)] for _ in range(4)]

#  Routing packet structure 
class RoutingPacket:
    def __init__(self, source_id, destination_id, minimum_costs):
        self.source_id = source_id
        self.destination_id = destination_id
        self.minimum_costs = minimum_costs[:]   # list of 4 minimum costs to each destination

#  Global event queue (simulates network layer delivery) 
packet_queue = []

def send_to_network_layer(packet):
    """Deliver packet to destination node (simulates the network layer)."""
    packet_queue.append(packet)


#  Helper: Compute current minimum costs from a node to all destinations 
def get_minimum_costs(node):
    """Return list of minimum costs from `node` to all destinations (0,1,2,3)."""
    return [min(routing_table[node][destination]) for destination in range(4)]


#  Initialization routines for each node

def initialize_routing_table(node):
    """Generic initialization routine for any node in the network."""
    # Identify all directly connected neighbors
    neighbors = [j for j in range(4) if LINK_COSTS[node][j] != INFINITY and j != node]

    # Initialize distance table with INFINITY values
    for destination in range(4):
        for via_neighbor in range(4):
            # Direct connection cost from node to destination via destination itself
            if via_neighbor == destination and LINK_COSTS[node][destination] != INFINITY:
                routing_table[node][destination][via_neighbor] = LINK_COSTS[node][destination]
            else:
                routing_table[node][destination][via_neighbor] = INFINITY
    # Cost to reach itself is always 0
    routing_table[node][node] = [0]*4

    print(f"\n[initialize{node}] Node {node} routing table initialized.")
    display_routing_table(node)

    # Send current minimum cost vector to each neighboring node
    current_costs = get_minimum_costs(node)
    for neighbor in neighbors:
        packet = RoutingPacket(source_id=node, destination_id=neighbor, minimum_costs=current_costs)
        send_to_network_layer(packet)
        print(f"  → Node {node} sends cost vector to Node {neighbor}: {current_costs}")


def initialize_routing_table0(): initialize_routing_table(0)
def initialize_routing_table1(): initialize_routing_table(1)
def initialize_routing_table2(): initialize_routing_table(2)
def initialize_routing_table3(): initialize_routing_table(3)


#  Update routines (Bellman-Ford equation execution)

def update_routing_table(node, packet):
    """Generic update routine that applies Bellman-Ford equation when receiving a routing packet."""
    sender = packet.source_id
    # Identify all directly connected neighbors
    neighbors = [j for j in range(4) if LINK_COSTS[node][j] != INFINITY and j != node]

    routing_changed = False
    
    # Apply Bellman-Ford equation: new_cost = direct_cost(node→sender) + sender's_cost_to_destination
    for destination in range(4):
        computed_cost = LINK_COSTS[node][sender] + packet.minimum_costs[destination]
        if computed_cost < routing_table[node][destination][sender]:
            routing_table[node][destination][sender] = computed_cost
            routing_changed = True

    print(f"\n[update{node}] Node {node} received routing update from Node {sender}.")
    display_routing_table(node)

    # If any minimum cost improved, propagate the updated information to neighbors
    if routing_changed:
        updated_costs = get_minimum_costs(node)
        for neighbor in neighbors:
            # Avoid sending back to the node that just sent us this update
            if neighbor != sender:
                outgoing_packet = RoutingPacket(source_id=node, destination_id=neighbor, minimum_costs=updated_costs)
                send_to_network_layer(outgoing_packet)
                print(f"  → Node {node} forwards updated cost vector to Node {neighbor}: {updated_costs}")


def update_routing_table0(packet): update_routing_table(0, packet)
def update_routing_table1(packet): update_routing_table(1, packet)
def update_routing_table2(packet): update_routing_table(2, packet)
def update_routing_table3(packet): update_routing_table(3, packet)



#  Display utility for routing tables

def display_routing_table(node):
    """Pretty-print the distance table for a given node."""
    print(f"  Distance Table at Node {node} (rows = destinations, columns = via neighbors):")
    column_header = "dest/via"
    header = f"  {column_header:>10}" + "".join(f"{'Node'+str(j):>10}" for j in range(4))
    print(header)
    print("  " + "-"*50)
    for destination in range(4):
        row = f"  {'Node'+str(destination):>10}"
        for via_neighbor in range(4):
            value = routing_table[node][destination][via_neighbor]
            row += f"{'INF':>10}" if value == INFINITY else f"{value:>10}"
        print(row)


#  Main simulation: Execute the distributed distance-vector algorithm

# Map destination node IDs to their respective update functions
UPDATE_HANDLERS = {
    0: update_routing_table0,
    1: update_routing_table1,
    2: update_routing_table2,
    3: update_routing_table3,
}

print("\n" + "="*60)
print("  PART 2: DISTANCE-VECTOR ROUTING (BELLMAN-FORD ALGORITHM)")
print("="*60)

# Step 1 – Initialize all nodes with their directly connected neighbors
print("\n--- Phase 1: Node Initialization ---")
initialize_routing_table0()
initialize_routing_table1()
initialize_routing_table2()
initialize_routing_table3()

# Step 2 – Process all routing packets until convergence (queue empty)
print("\n--- Phase 2: Route Propagation and Convergence ---")
iteration_counter = 0
while packet_queue:
    iteration_counter += 1
    current_packet = packet_queue.pop(0)
    print(f"\n[Iteration {iteration_counter}] Delivering packet: Node {current_packet.source_id} → Node {current_packet.destination_id}")
    UPDATE_HANDLERS[current_packet.destination_id](current_packet)

# Step 3 – Display final routing tables after algorithm convergence
print("\n" + "="*60)
print("  FINAL ROUTING TABLES (After Distance-Vector Algorithm Convergence)")
print("="*60)
for node in range(4):
    minimum_costs = get_minimum_costs(node)
    neighbors = [j for j in range(4) if LINK_COSTS[node][j] != INFINITY and j != node]
    print(f"\n  Node {node} — Final Routing Table:")
    print(f"  {'Destination':<15} {'Next Hop':<12} {'Minimum Cost'}")
    print(f"  {'-'*42}")
    for destination in range(4):
        if destination == node:
            continue
        # Determine next hop: neighbor that provides the minimum cost to this destination
        best_next_hop = min(neighbors, key=lambda neighbor: routing_table[node][destination][neighbor])
        best_path_cost = routing_table[node][destination][best_next_hop]
        print(f"  {destination:<15} {best_next_hop:<12} {best_path_cost}")

print("\n" + "="*60 + "\n")