# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def or_gate(a, b):
    dev = qml.device("default.qubit", wires=9, shots=None)
    
    @qml.qnode(dev)
    def circuit():
        # Initialize registers
        qr_a = [0, 1, 2]
        qr_b = [3, 4, 5]
        ancillary = [6, 7, 8]
        
        # Format inputs to 3-bit binary
        a_bin = format(a, '03b')
        b_bin = format(b, '03b')
        
        # Apply X gates based on input values
        for i in range(3):
            if a_bin[2-i] == '0':
                qml.PauliX(wires=qr_a[i])
            if b_bin[2-i] == '0':
                qml.PauliX(wires=qr_b[i])
        
        # Apply CCNOT (Toffoli) gates
        for i in range(3):
            qml.Toffoli(wires=[qr_a[i], qr_b[i], ancillary[i]])
        
        # Apply X to ancillary register
        for i in range(3):
            qml.PauliX(wires=ancillary[i])
        
        return qml.sample(wires=ancillary)
    
    # Run the circuit multiple times to get samples
    samples = circuit()
    if len(samples.shape) == 1:
        # Single sample case
        samples = samples.reshape(1, -1)
    
    # Convert samples to bit strings
    bit_strings = []
    for sample in samples:
        bit_str = ''.join(['1' if s > 0.5 else '0' for s in sample])
        bit_strings.append(bit_str)
    
    # Count occurrences
    counts = Counter(bit_strings)
    total = sum(counts.values())
    
    # Convert to probabilities
    prob_dist = {key: value / total for key, value in counts.items()}
    
    return prob_dist
