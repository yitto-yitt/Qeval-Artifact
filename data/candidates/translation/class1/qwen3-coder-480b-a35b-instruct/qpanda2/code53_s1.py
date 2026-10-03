# EVAL_META: task_id=53, framework=qpanda2, class=1
import pyqpanda as pq
import numpy as np
from pyqpanda import *
import builtins

def xor_gate(a, b):
    # Create a quantum program
    prog = QProg()
    
    # Create 9 qubits (8 for data + 1 ancilla for XOR operation)
    qubits = pq.qAlloc_many(8)
    
    # Initialize qubits based on bits of a
    for i in range(8):
        if (a >> i) & 1:
            prog << X(qubits[i])
    
    # Apply XOR with b
    for i in range(8):
        if (b >> i) & 1:
            prog << X(qubits[i])
    
    # Measure all qubits
    cbits = pq.cAlloc_many(8)
    for i in range(8):
        prog << Measure(qubits[i], cbits[i])
    
    # Run the program
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    # Simulate multiple shots to get probability distribution
    shots = 1024
    result = machine.run_with_configuration(prog, cbits, shots)
    
    # Process the results
    counts = {}
    for outcome, count in result.items():
        # Convert outcome string to 8-bit binary string
        outcome_bin = format(int(outcome), '08b')
        counts[outcome_bin] = count
    
    # Calculate probabilities
    total = builtins.sum(counts.values())
    probabilities = {key: value / total for key, value in counts.items()}
    
    machine.destroy_qvm()
    
    return probabilities
