# EVAL_META: task_id=54, framework=qpanda2, class=1
import pyqpanda as pq
import numpy as np

def and_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(9)  # 3 for a, 3 for b, 3 for ancillary
    cbits = machine.cAlloc_many(3)   # 3 classical bits for measurement
    
    prog = pq.QProg()
    
    # Initialize input values
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    # Apply X gates to set initial state based on input values
    for i in range(3):
        if a_str[2-i] == '1':
            prog.insert(pq.X(qubits[i]))
        if b_str[2-i] == '1':
            prog.insert(pq.X(qubits[i+3]))
    
    # Apply CCX (Toffoli) gates for AND operation
    for i in range(3):
        prog.insert(pq.Toffoli(qubits[i], qubits[i+3], qubits[i+6]))
    
    # Measure ancillary qubits
    for i in range(3):
        prog.insert(pq.Measure(qubits[i+6], cbits[i]))
    
    # Run the program
    result = machine.run_with_configuration(prog, cbits, 1024)
    
    # Process results
    total_shots = 1024  # Number of shots used
    prob_dist = {}
    
    # Convert result dictionary keys to 3-bit strings
    for key, value in result.items():
        # Format the key to be a 3-bit string
        formatted_key = format(int(key), '03b')[-3:]
        prob_dist[formatted_key] = value / total_shots
    
    machine.finalize()
    
    return prob_dist
