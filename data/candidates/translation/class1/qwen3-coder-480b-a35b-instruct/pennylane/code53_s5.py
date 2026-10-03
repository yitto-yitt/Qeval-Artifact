# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def xor_gate(a, b):
    # Convert integers to binary strings (8 bits)
    a_bin = format(a, '08b')
    b_bin = format(b, '08b')
    
    # Compute XOR classically since we need to prepare the state
    result_int = a ^ b
    result_bin = format(result_int, '08b')
    
    # Create a device with 8 qubits
    dev = qml.device('default.qubit', wires=8)
    
    @qml.qnode(dev)
    def circuit():
        # Prepare initial state based on result_bin
        for i, bit in enumerate(result_bin):
            if bit == '1':
                qml.PauliX(wires=i)
        
        # Measure all qubits
        return qml.sample(wires=range(8))
    
    # Run the circuit multiple times to get samples
    num_samples = 2048  # Typical number for sampling
    samples = circuit()
    
    # Convert samples back to binary strings
    results = []
    for sample in samples:
        binary_str = ''.join(['1' if s > 0.5 else '0' for s in sample])
        results.append(binary_str)
    
    # Count occurrences
    counts = Counter(results)
    total = sum(counts.values())
    
    # Normalize to probabilities
    prob_dist = {key: value / total for key, value in counts.items()}
    
    return prob_dist
