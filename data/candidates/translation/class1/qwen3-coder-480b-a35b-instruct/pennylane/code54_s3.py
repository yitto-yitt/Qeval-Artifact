# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def and_gate(a, b):
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    
    dev = qml.device('default.qubit', wires=9, shots=10000)
    
    @qml.qnode(dev)
    def circuit():
        # Initialize input registers
        for i in range(3):
            if a_bits[2-i] == '1':
                qml.PauliX(wires=i)  # qr_a[0:3]
            if b_bits[2-i] == '1':
                qml.PauliX(wires=i+3)  # qr_b[3:6]
        
        # Apply CCNOT (Toffoli) gates for AND operation
        for i in range(3):
            qml.Toffoli(wires=[i, i+3, i+6])  # ancillary at [6:9]
        
        # Measure the ancillary qubits (output of AND)
        return qml.sample(wires=[6, 7, 8])
    
    samples = circuit()
    
    # Convert samples to bitstrings and count occurrences
    bitstrings = [''.join(map(str, sample)) for sample in samples]
    counts = Counter(bitstrings)
    
    # Normalize to get probabilities
    total = len(samples)
    prob_dist = {bitstring: count/total for bitstring, count in counts.items()}
    
    return prob_dist
