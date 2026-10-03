# EVAL_META: task_id=54, framework=qpanda2, class=1
import pyqpanda as pq
import numpy as np
import math

def and_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(9)  # 3 for a, 3 for b, 3 for ancillary
    
    prog = pq.QProg()
    
    # Format inputs as 3-bit binary strings
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    # Initialize input states
    for i in range(3):
        if a_str[2-i] == '1':
            prog << pq.X(qubits[i])  # First 3 qubits for a
        if b_str[2-i] == '1':
            prog << pq.X(qubits[i+3])  # Next 3 qubits for b
    
    # Perform AND operation using Toffoli gates
    for i in range(3):
        prog << pq.TOFFOLI(qubits[i], qubits[i+3], qubits[i+6])  # ancillary qubits at index 6,7,8
    
    # Measure ancillary qubits (last 3)
    c = machine.cAlloc_many(3)
    for i in range(3):
        prog << pq.Measure(qubits[i+6], c[i])
    
    result = machine.run_with_configuration(prog, c, 1024)
    
    # Calculate probabilities
    total_shots = 1024
    prob_dist = {}
    for outcome, count in result.items():
        prob_dist[outcome] = count / total_shots
        
    machine.finalize()
    return prob_dist
