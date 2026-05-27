"""
Question 3: Head-of-Line (HOL) Blocking — Markov Chain Verification
2x2 switch configuration, state space represents buffer occupancies: {11, 12, 21, 22}
- State '11': Both input ports have packet for output port 1
- State '12': Input port 1 has packet for output 1, input port 2 has packet for output 2
- State '21': Input port 1 has packet for output 2, input port 2 has packet for output 1
- State '22': Both input ports have packet for output port 2
"""

import numpy as np

#  Transition Probability Matrix 
# State encoding: 0='11', 1='12', 2='21', 3='22'
transition_matrix = np.array([
    [1/2, 1/4, 1/4,   0],   # transitions from state '11'
    [1/4, 1/4, 1/4, 1/4],   # transitions from state '12'
    [1/4, 1/4, 1/4, 1/4],   # transitions from state '21'
    [  0, 1/4, 1/4, 1/2],   # transitions from state '22'
])

STATE_LABELS = ['11', '12', '21', '22']

#  Display Transition Matrix 
print("=" * 55)
print("  HOL BLOCKING ANALYSIS — 2x2 Switch Markov Chain")
print("=" * 55)

print("\n1. Transition Probability Matrix P:")
print(f"   {'':6}", end="")
for label in STATE_LABELS:
    print(f"{'to '+label:>8}", end="")
print()
print(f"   {'-'*38}")
for idx, row in enumerate(transition_matrix):
    print(f"   from {STATE_LABELS[idx]}: ", end="")
    for probability in row:
        print(f"{probability:>8.4f}", end="")
    print()

#  Method 1: Analytical Solution — Solving πP = π ─
# Equation: πP = π  →  π(P - I)ᵀ = 0
# Replace last equation with normalization constraint: Σπ = 1

coefficient_matrix = (transition_matrix.T - np.eye(4))
coefficient_matrix[-1, :] = 1          # Overwrite last row with normalization constraint
constant_vector = np.zeros(4)
constant_vector[-1] = 1                # Sum of probabilities equals 1

stationary_distribution_analytical = np.linalg.solve(coefficient_matrix, constant_vector)

print("\n2. Stationary Distribution (Analytical Method — solving πP = π):")
print(f"   {'State':<10} {'π Probability':<14} {'Fraction'}")
print(f"   {'-'*38}")
for idx, label in enumerate(STATE_LABELS):
    print(f"   {label:<10} {stationary_distribution_analytical[idx]:<14.6f} {round(stationary_distribution_analytical[idx], 4)}")

#  Method 2: Power Iteration — Computing P^n converges to stationary distribution ─
power_matrix = np.linalg.matrix_power(transition_matrix, 1000)
stationary_power_iter = power_matrix[0]      # Any row converges to the stationary distribution

print("\n3. Stationary Distribution (Power Iteration — P^1000):")
print(f"   {'State':<10} {'π Probability':<14} {'Fraction'}")
print(f"   {'-'*38}")
for idx, label in enumerate(STATE_LABELS):
    print(f"   {label:<10} {stationary_power_iter[idx]:<14.6f} {round(stationary_power_iter[idx], 4)}")

#  Method 3: Monte Carlo Simulation 
import random
random.seed(42)          # Fixed seed for reproducible results

NUM_SIMULATION_STEPS = 1_000_000
current_state = 0        # Start from state '11'
state_visit_counts = [0, 0, 0, 0]
total_packets_transmitted = 0

for _ in range(NUM_SIMULATION_STEPS):
    state_visit_counts[current_state] += 1
    
    # Count packets transmitted in this time slot
    if current_state == 0 or current_state == 3:   # State '11' or '22' → collision, only 1 packet sent
        total_packets_transmitted += 1
    else:                                            # State '12' or '21' → no collision, 2 packets sent
        total_packets_transmitted += 2
    
    # Transition to next state based on probabilities
    random_value = random.random()
    cumulative_probability = 0
    for next_state, transition_prob in enumerate(transition_matrix[current_state]):
        cumulative_probability += transition_prob
        if random_value < cumulative_probability:
            current_state = next_state
            break

simulated_distribution = [count / NUM_SIMULATION_STEPS for count in state_visit_counts]

print(f"\n4. Stationary Distribution (Monte Carlo Simulation — {NUM_SIMULATION_STEPS:,} steps):")
print(f"   {'State':<10} {'π (Simulated)':<16} {'π (Exact)'}")
print(f"   {'-'*42}")
for idx, label in enumerate(STATE_LABELS):
    print(f"   {label:<10} {simulated_distribution[idx]:<16.6f} {stationary_distribution_analytical[idx]:.6f}")

#  Throughput Calculation ─
# Packets transmitted per time slot: 1 packet for collision states (11 or 22), 2 packets for non-collision states (12 or 21)
packets_per_state = [1, 2, 2, 1]

# Analytical throughput
throughput_analytical = sum(stationary_distribution_analytical[i] * packets_per_state[i] for i in range(4))

# Simulated throughput
throughput_simulated = total_packets_transmitted / NUM_SIMULATION_STEPS

print("\n" + "=" * 55)
print("5. Average Throughput Analysis:")
print(f"   Analytical Throughput    : {throughput_analytical:.6f} packets/time slot")
print(f"   Simulated Throughput     : {throughput_simulated:.6f} packets/time slot")
print(f"   Maximum possible (no HOL blocking): 2.0 packets/time slot")
print(f"   Switch Efficiency        : {throughput_analytical/2*100:.1f}%")
print(f"   Performance loss due to HOL: {(1 - throughput_analytical/2)*100:.1f}%")
print("=" * 55)

#  Verification: Check if πP = π holds ─
piP_check = stationary_distribution_analytical @ transition_matrix
print("\n6. Verification of Stationary Distribution (πP should equal π):")
print(f"   π (computed)           = {stationary_distribution_analytical.round(6)}")
print(f"   πP (computed)          = {piP_check.round(6)}")
print(f"   Distribution matches?  : {np.allclose(stationary_distribution_analytical, piP_check)}")
print(f"   Sum of probabilities   : {stationary_distribution_analytical.sum():.6f} (should equal 1.0)")