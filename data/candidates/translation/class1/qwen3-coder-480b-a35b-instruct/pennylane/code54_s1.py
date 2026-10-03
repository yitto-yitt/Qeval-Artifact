# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml
from collections import defaultdict

def and_gate(a, b):
    dev = qml.device("default.qubit", wires=9, shots=1000)

    @qml.qnode(dev)
    def circuit(a_bits, b_bits):
        # Encode input bits
        for i in range(3):
            if a_bits[2-i] == '1':
                qml.PauliX(wires=i)
            if b_bits[2-i] == '1':
                qml.PauliX(wires=i+3)
        
        # Perform bitwise AND using Toffoli gates
        for i in range(3):
            qml.Toffoli(wires=[i, i+3, i+6])
        
        return qml.sample(wires=[6, 7, 8])

    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    
    samples = circuit(a_bits, b_bits)
    
    # Convert samples to bitstrings and count
    counts = defaultdict(int)
    for sample in samples:
        bitstring = ''.join(str(int(bit)) for bit in sample)
        counts[bitstring] += 1
    
    # Normalize to get probabilities
    total = len(samples)
    return {key: value / total for key, value in counts.items()}
