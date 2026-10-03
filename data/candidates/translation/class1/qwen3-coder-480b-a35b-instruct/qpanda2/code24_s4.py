# EVAL_META: task_id=24, framework=qpanda2, class=1
import pyqpanda as pq
from pyqpanda import *
import math

def dj_algorithm(oracle):
    # Get the number of qubits from the oracle
    n = oracle.qubit_num()
    
    # Create quantum and classical registers
    machine = init_quantum_machine(QMachineType.CPU)
    qvec = machine.qAlloc_many(n)
    cvec = machine.cAlloc_many(n - 1)
    
    # Build the circuit
    prog = QProg()
    
    # Initialize the last qubit to |1> (equivalent to x gate)
    prog << X(qvec[n - 1])
    
    # Apply Hadamard to all qubits
    for i in range(n):
        prog << H(qvec[i])
    
    # Add the oracle
    prog << oracle
    
    # Apply Hadamard to all qubits again
    for i in range(n):
        prog << H(qvec[i])
    
    # Measure the first n-1 qubits
    for i in range(n - 1):
        prog << Measure(qvec[i], cvec[i])
    
    # Run the program
    result = machine.run(prog)
    
    # Get measurement results
    counts = result
    total_shots = 0
    for count in counts.values():
        total_shots += count
        
    # Calculate probabilities
    prob_dist = {}
    for key, value in counts.items():
        prob_dist[key] = value / total_shots
    
    destroy_quantum_machine(machine)
    return prob_dist
