# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def xor_gate(a, b):
    # Convert integers to binary strings (8 bits)
    a_bin = format(a, '08b')
    b_bin = format(b, '08b')
    
    # Compute XOR classically since it's a deterministic operation
    result_int = a ^ b
    result_bin = format(result_int, '08b')
    
    # Since this is deterministic, we just need to return the single outcome
    # with probability 1.0, but we'll simulate it properly with PennyLane
    dev = qml.device('default.qubit', wires=8)
    
    @qml.qnode(dev)
    def circuit():
        # Prepare initial state based on a and b
        for i in range(8):
            if a_bin[i] == '1':
                qml.PauliX(wires=i)
        
        # Apply XOR operation: for each bit where b has 1, flip the corresponding qubit
        for i in range(8):
            if b_bin[i] == '1':
                qml.PauliX(wires=i)
        
        return [qml.sample(qml.PauliZ(i)) for i in range(8)]
    
    # Run the circuit multiple times to get samples
    samples = circuit()
    # Convert samples to bit strings
    bit_strings = []
    for shot_samples in zip(*samples):
        bit_string = ''.join(['0' if s == 1 else '1' for s in shot_samples])
        bit_strings.append(bit_string)
    
    # Count occurrences
    counts = Counter(bit_strings)
    total = sum(counts.values())
    
    # Normalize to probabilities
    prob_dist = {key: value / total for key, value in counts.items()}
    
    return prob_dist
