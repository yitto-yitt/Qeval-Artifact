# EVAL_META: task_id=55, framework=qpanda2, class=1
import pyqpanda as pq
import numpy as np

def or_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(9)  # 3 for a, 3 for b, 3 for ancillary
    cbits = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    
    # Initialize a and b registers
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2-i] == '0':
            prog << pq.X(qubits[i])
        if b_str[2-i] == '0':
            prog << pq.X(qubits[i+3])
    
    # Apply CCX gates (Toffoli gates) to compute AND of each bit pair
    for i in range(3):
        prog << pq.CCX(qubits[i], qubits[i+3], qubits[i+6])
    
    # Apply X gate to ancillary qubits to get OR instead of AND
    for i in range(3):
        prog << pq.X(qubits[i+6])
    
    # Measure the ancillary qubits
    for i in range(3):
        prog << pq.Measure(qubits[i+6], cbits[i])
    
    result = pq.run_with_configuration(prog, machine, shots=1024)
    
    # Calculate total shots
    import builtins
    total_shots = builtins.sum(result.values())
    
    # Normalize the counts to get probabilities
    prob_dist = {}
    for key, value in result.items():
        prob_dist[key] = value / total_shots
    
    machine.finalize()
    return prob_dist
