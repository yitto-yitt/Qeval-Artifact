# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def and_gate(a, b):
    dev = qml.device("default.qubit", wires=9, shots=10000)
    
    @qml.qnode(dev)
    def circuit():
        # Initialize input states
        a_bin = format(a, '03b')
        b_bin = format(b, '03b')
        
        # Apply X gates to set initial states for a
        for i in range(3):
            if a_bin[2-i] == '1':
                qml.PauliX(wires=i)  # First 3 wires for a
        
        # Apply X gates to set initial states for b
        for i in range(3):
            if b_bin[2-i] == '1':
                qml.PauliX(wires=i+3)  # Next 3 wires for b
        
        # Apply CCNOT (Toffoli) gates for AND operation
        for i in range(3):
            qml.Toffoli(wires=[i, i+3, i+6])  # CCX: control1=a[i], control2=b[i], target=ancilla[i]
        
        # Measure the ancillary qubits (last 3 wires)
        return qml.sample(wires=[6, 7, 8])
    
    samples = circuit()
    
    # Convert samples to binary strings and count occurrences
    if len(samples.shape) == 1:
        # Single sample case - convert to 2D array
        samples = samples.reshape(-1, 3)
    
    bit_strings = []
    for sample in samples:
        bit_string = ''.join(str(int(bit)) for bit in sample)
        bit_strings.append(bit_string)
    
    counts = Counter(bit_strings)
    total = sum(counts.values())
    
    # Normalize to get probabilities
    prob_dist = {key: value / total for key, value in counts.items()}
    
    return prob_dist
