# EVAL_META: task_id=53, framework=qpanda2, class=1
import pyqpanda as pq
import math

def xor_gate(a, b):
    # Create a quantum machine
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(8)
    cbits = machine.cAlloc_many(8)
    
    # Initialize the quantum program
    prog = pq.QProg()
    
    # Apply X gates based on bits set in 'a'
    for i in range(8):
        if (a >> i) & 1:
            prog.insert(pq.X(qubits[i]))
    
    # Apply X gates based on bits set in 'b'  
    for i in range(8):
        if (b >> i) & 1:
            prog.insert(pq.X(qubits[i]))
    
    # Measure all qubits
    for i in range(8):
        prog.insert(pq.Measure(qubits[i], cbits[i]))
    
    # Run the program
    result = machine.run(prog)
    
    # Convert result to counts
    counts = {}
    for bit_str, count in result.items():
        # Reverse the bit string to match Qiskit's convention
        reversed_bit_str = bit_str[::-1]
        counts[reversed_bit_str] = count
    
    # Calculate probabilities
    import builtins
    total_shots = builtins.sum(counts.values())
    prob_dist = {key: value / total_shots for key, value in counts.items()}
    
    # Free allocated resources
    machine.finalize()
    
    return prob_dist
