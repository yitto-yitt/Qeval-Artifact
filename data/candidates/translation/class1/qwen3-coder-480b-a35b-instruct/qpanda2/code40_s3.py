# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda as pq
import numpy as np
import builtins

def init_random_3qubit(desired_vector):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    
    # Create quantum circuit
    prog = pq.QProg()
    
    # Initialize the state
    # In pyqpanda, we need to decompose the desired vector into gates
    # Using U3 gates to prepare arbitrary states
    sv = pq.StateVector(desired_vector)
    init_gate = pq.create_init_state(sv)
    prog.insert(init_gate)
    
    # Measure all qubits
    for i in range(3):
        prog.insert(pq.Measure(qubits[i], pq.QVec()))
    
    # Run the program
    result = machine.run_with_configuration(prog, qubits, 1000)  # Using 1000 shots as default
    
    # Process results
    total_shots = 1000  # Number of shots used
    counts = {}
    for key, value in result.items():
        # Reverse the bitstring to match Qiskit's convention (most significant bit first)
        reversed_key = key[::-1]
        counts[reversed_key] = value
    
    # Calculate probabilities
    total = builtins.sum(counts.values())
    if total == 0:
        total = total_shots
    
    prob_dist = {key: value / total for key, value in counts.items()}
    
    machine.finalize()
    return prob_dist
