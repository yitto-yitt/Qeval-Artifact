# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml
from collections import defaultdict

def or_gate(a, b):
    dev = qml.device("default.qubit", wires=9, shots=1000)
    
    @qml.qnode(dev)
    def circuit(a_bits, b_bits):
        # Encode input bits
        for i in range(3):
            if a_bits[2-i] == '0':
                qml.PauliX(wires=i)
            if b_bits[2-i] == '0':
                qml.PauliX(wires=i+3)
        
        # Perform OR operation using ancillary qubits
        for i in range(3):
            # Use Toffoli gates to compute AND, then apply X to get OR
            qml.Toffoli(wires=[i, i+3, i+6])
        
        # Apply X to get the OR result (since we computed AND)
        qml.PauliX(wires=6)
        qml.PauliX(wires=7)
        qml.PauliX(wires=8)
        
        return qml.sample(wires=[6, 7, 8])
    
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    
    samples = circuit(a_bits, b_bits)
    
    # Convert samples to bitstrings and count occurrences
    counts = defaultdict(int)
    for sample in samples:
        bitstring = ''.join(str(int(bit)) for bit in sample)
        counts[bitstring] += 1
    
    # Normalize to get probabilities
    total = len(samples)
    return {key: value / total for key, value in counts.items()}
