# EVAL_META: task_id=53, framework=qpanda2, class=1
import pyqpanda as pq
import math

def xor_gate(a, b):
    # Create a quantum machine
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    
    # Allocate 9 qubits (8 for data + 1 ancilla for XOR operation)
    qubits = machine.qAlloc_many(9)
    cbits = machine.cAlloc_many(8)
    
    # Initialize quantum program
    prog = pq.QProg()
    
    # Apply X gates to set initial values based on bits of a and b
    for i in range(8):
        if (a >> i) & 1:
            prog.insert(pq.X(qubits[i]))
    
    # Perform XOR operation: result = a XOR b
    for i in range(8):
        control_bit = (b >> i) & 1
        if control_bit:
            prog.insert(pq.CNOT(qubits[i], qubits[8]))  # Use ancilla qubit temporarily
    
    # Now we need to implement XOR more directly
    # Reset the program for a cleaner implementation
    prog = pq.QProg()
    
    # Set up initial state based on a
    for i in range(8):
        if (a >> i) & 1:
            prog.insert(pq.X(qubits[i]))
    
    # Apply XOR: for each bit position, if b has a 1, flip that bit in the result
    for i in range(8):
        if (b >> i) & 1:
            prog.insert(pq.X(qubits[i]))
    
    # Measure all 8 data qubits
    for i in range(8):
        prog.insert(pq.Measure(qubits[i], cbits[i]))
    
    # Run the program
    result = pq.run_with_configuration(prog, machine, shots=1024)
    
    # Calculate total shots
    import builtins
    total_shots = builtins.sum(result.values())
    
    # Normalize the counts to get probabilities
    prob_dist = {}
    for outcome, count in result.items():
        prob_dist[outcome] = count / total_shots
    
    # Release resources
    machine.finalize()
    
    return prob_dist
