# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml
from collections import defaultdict

def not_gate(a):
    dev = qml.device("default.qubit", wires=8, shots=1000)
    
    @qml.qnode(dev)
    def circuit():
        # Prepare the input state
        a_bits = format(a, "08b")
        for i in range(8):
            if a_bits[7-i] == "1":
                qml.PauliX(wires=i)
        
        # Apply NOT gates (PauliX) to all qubits
        for i in range(8):
            qml.PauliX(wires=i)
        
        return qml.sample(wires=range(8))
    
    # Run the circuit and collect samples
    samples = circuit()
    
    # Convert samples to bitstrings and count occurrences
    counts = defaultdict(int)
    for sample in samples:
        # Convert array of 0s and 1s to bitstring
        bitstring = ''.join(str(int(bit)) for bit in sample)
        counts[bitstring] += 1
    
    # Normalize to get probabilities
    total = sum(counts.values())
    probabilities = {key: value / total for key, value in counts.items()}
    
    return probabilities
