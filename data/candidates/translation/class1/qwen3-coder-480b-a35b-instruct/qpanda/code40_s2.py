# EVAL_META: task_id=40, framework=qpanda, class=1
import pyqpanda3.core as pq
import numpy as np

def init_random_3qubit(desired_vector):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    
    # Create quantum program to initialize the state
    prog = pq.QProg()
    
    # Initialize the quantum state using the desired vector
    init_gates = pq.initState(qubits, desired_vector)
    prog.insert(init_gates)
    
    # Measure all qubits
    cbits = [machine.cAlloc() for _ in range(3)]
    for i in range(3):
        prog.insert(pq.Measure(qubits[i], cbits[i]))
    
    # Run the program multiple times to get statistics
    result = machine.run_with_configuration(prog, cbits, 1000)
    
    # Convert results to probability distribution
    total_shots = 1000
    counts = {}
    for outcome, count in result.items():
        # Reverse the bitstring to match qiskit's convention (most significant bit first)
        reversed_outcome = outcome[::-1]
        counts[reversed_outcome] = count
    
    # Normalize counts to probabilities
    prob_dist = {}
    for key, value in counts.items():
        prob_dist[key] = value / total_shots
    
    # Ensure all 8 possible outcomes are represented (some may have 0 probability)
    all_outcomes = [format(i, '03b') for i in range(8)]
    for outcome in all_outcomes:
        if outcome not in prob_dist:
            prob_dist[outcome] = 0.0
    
    machine.finalize()
    return prob_dist
