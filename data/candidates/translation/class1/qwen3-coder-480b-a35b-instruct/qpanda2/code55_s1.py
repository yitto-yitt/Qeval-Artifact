# EVAL_META: task_id=55, framework=qpanda2, class=1
import pyqpanda as pq
import numpy as np

def or_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(9)  # 3 for a, 3 for b, 3 for ancillary
    c = machine.cAlloc_many(3)
    
    qr_a = qubits[:3]
    qr_b = qubits[3:6]
    ancillary = qubits[6:9]
    
    prog = pq.QProg()
    
    # Format a and b to 3-bit binary strings
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    # Initialize input states (flip bits where needed)
    for i in range(3):
        if a_str[2-i] == '0':
            prog << pq.X(qr_a[i])
        if b_str[2-i] == '0':
            prog << pq.X(qr_b[i])
    
    # Apply CCX gates to compute AND of each bit pair
    for i in range(3):
        prog << pq.CCX(qr_a[i], qr_b[i], ancillary[i])
    
    # Flip all ancillary qubits to get OR instead of NAND
    for i in range(3):
        prog << pq.X(ancillary[i])
    
    # Measure ancillary qubits
    for i in range(3):
        prog << pq.Measure(ancillary[i], c[i])
    
    # Run the program
    result = machine.run_with_configuration(prog, c, 1024)
    
    # Calculate total shots
    import builtins
    total_shots = builtins.sum(result.values())
    
    # Normalize the counts to get probabilities
    prob_dist = {}
    for key, value in result.items():
        prob_dist[key] = value / total_shots
    
    machine.finalize()
    return prob_dist
