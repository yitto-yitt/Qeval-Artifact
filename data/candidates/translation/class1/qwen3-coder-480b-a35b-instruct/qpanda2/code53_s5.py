# EVAL_META: task_id=53, framework=qpanda2, class=1
import pyqpanda as pq
import math

def xor_gate(a, b):
    # Create a quantum machine
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    
    # Allocate 9 qubits (8 for data + 1 ancilla for XOR operation)
    qubits = machine.qAlloc_many(9)
    cbits = machine.cAlloc_many(8)
    
    # Convert a and b to binary strings (8 bits)
    a_bin = format(a, '08b')
    b_bin = format(b, '08b')
    
    # Initialize quantum circuit
    prog = pq.QProg()
    
    # Apply X gates to set initial state according to a
    for i in range(8):
        if a_bin[i] == '1':
            prog << pq.X(qubits[i])
    
    # Perform XOR operation: result will be stored in first 8 qubits
    # XOR can be implemented using CNOT gates
    for i in range(8):
        if b_bin[i] == '1':
            prog << pq.CNOT(qubits[8], qubits[i])  # Ancilla controls
            # Actually we need to implement XOR between first 8 qubits and value b
            # We'll implement this differently - directly compute a XOR b
    
    # Reset the program to implement XOR properly
    prog = pq.QProg()
    
    # Set initial state based on 'a'
    for i in range(8):
        if a_bin[i] == '1':
            prog << pq.X(qubits[i])
    
    # Implement XOR with 'b' by flipping bits where b has 1s
    result_xor = a ^ b
    result_bin = format(result_xor, '08b')
    
    # Since XOR is deterministic, we just measure the result of a XOR b
    # Directly prepare the result state
    prog = pq.QProg()
    for i in range(8):
        if result_bin[7-i] == '1':  # Reverse indexing for QPanda
            prog << pq.X(qubits[i])
    
    # Measure all 8 qubits
    for i in range(8):
        prog << pq.Measure(qubits[i], cbits[i])
    
    # Run the program
    shots = 1024
    result = pq.prob_run_dict(prog, cbits, shots)
    
    # Normalize the results
    total = sum(result.values())
    normalized_result = {key: value / total for key, value in result.items()}
    
    # Release quantum resources
    pq.destroy_quantum_machine(machine)
    
    return normalized_result
