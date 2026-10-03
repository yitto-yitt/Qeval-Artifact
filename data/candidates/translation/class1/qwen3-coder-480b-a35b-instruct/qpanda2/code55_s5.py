# EVAL_META: task_id=55, framework=qpanda2, class=1
import pyqpanda as pq
import numpy as np

def or_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(9)  # 3 for a, 3 for b, 3 for ancillary
    
    prog = pq.QProg()
    
    # Format inputs as 3-bit binary strings
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    # Initialize input qubits - flip if bit is 0 (to simulate |0> initially)
    for i in range(3):
        if a_bin[2-i] == '0':
            prog << pq.X(qubits[i])  # First 3 qubits for a
        if b_bin[2-i] == '0':
            prog << pq.X(qubits[i+3])  # Next 3 qubits for b
    
    # Apply CCX gates to compute AND of each pair of bits
    for i in range(3):
        prog << pq.CCX(qubits[i], qubits[i+3], qubits[i+6])  # ancillary qubits at index 6,7,8
    
    # Flip all ancillary qubits to get OR instead of NAND
    for i in range(3):
        prog << pq.X(qubits[i+6])
    
    # Measure ancillary qubits
    c = machine.cAlloc_many(3)
    for i in range(3):
        prog << pq.Measure(qubits[i+6], c[i])
    
    # Run the program
    result = machine.run_with_configuration(prog, c, 1024)
    
    # Process results
    import builtins
    total_shots = builtins.sum(result.values())
    prob_dist = {key: value / total_shots for key, value in result.items()}
    
    machine.finalize()
    return prob_dist
