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
        
        # Apply X gates to set initial states based on a and b
        for i in range(3):
            if a_bin[2-i] == '1':
                qml.PauliX(wires=i)  # First 3 wires for a
            if b_bin[2-i] == '1':
                qml.PauliX(wires=i+3)  # Next 3 wires for b
        
        # Perform AND operations using Toffoli gates (CCNOT)
        for i in range(3):
            qml.Toffoli(wires=[i, i+3, i+6])  # ancilla at i+6
        
        # Measure the ancillary qubits (last 3 wires)
        return qml.sample(wires=[6, 7, 8])
    
    samples = circuit()
    
    # Convert samples to bit strings and count occurrences
    bit_strings = []
    for sample in samples:
        bit_str = ''.join(str(int(bit)) for bit in sample)
        bit_strings.append(bit_str)
    
    counts = Counter(bit_strings)
    total = sum(counts.values())
    
    # Normalize to get probabilities
    prob_dist = {key: value / total for key, value in counts.items()}
    
    return prob_dist
