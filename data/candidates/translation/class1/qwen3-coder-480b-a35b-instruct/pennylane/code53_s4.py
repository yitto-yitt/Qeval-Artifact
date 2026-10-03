# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def xor_gate(a, b):
    # Convert integers to binary strings (8 bits)
    a_bin = format(a, '08b')
    b_bin = format(b, '08b')
    
    # Calculate XOR manually
    result_bin = ''
    for i in range(8):
        bit_a = int(a_bin[i])
        bit_b = int(b_bin[i])
        xor_bit = bit_a ^ bit_b
        result_bin += str(xor_bit)
    
    # Create a device with 8 wires
    dev = qml.device('default.qubit', wires=8)
    
    @qml.qnode(dev)
    def circuit():
        # Initialize the state to represent the XOR result
        for i in range(8):
            if result_bin[7-i] == '1':  # Reverse indexing for little-endian
                qml.PauliX(wires=i)
        
        # Measure all wires
        return [qml.sample(qml.PauliZ(i)) for i in range(8)]
    
    # Run the circuit multiple times to get samples
    samples = circuit()
    # Convert samples to binary strings
    binary_strings = []
    for shot_samples in zip(*samples):
        binary_str = ''
        for s in shot_samples:
            # Convert -1 to 0, 1 to 1
            bit = '0' if s == -1 else '1'
            binary_str = bit + binary_str  # Reverse order to match expected format
        binary_strings.append(binary_str)
    
    # Count occurrences
    counts = Counter(binary_strings)
    total = sum(counts.values())
    
    # Normalize to probabilities
    prob_dist = {key: value / total for key, value in counts.items()}
    
    return prob_dist
