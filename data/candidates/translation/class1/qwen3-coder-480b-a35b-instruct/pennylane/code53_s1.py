# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml
from collections import defaultdict

def xor_gate(a, b):
    # Create a device with 8 wires (qubits)
    dev = qml.device('default.qubit', wires=8, shots=1000)
    
    @qml.qnode(dev)
    def circuit():
        # Encode the first integer 'a' into the qubits
        for i in range(8):
            if (a >> i) & 1:
                qml.PauliX(wires=i)
        
        # Apply XOR with 'b' - this is done by applying PauliX gates
        # on qubits where the corresponding bit of b is 1
        for i in range(8):
            if (b >> i) & 1:
                qml.PauliX(wires=i)
        
        # Measure all qubits
        return qml.sample(wires=range(8))
    
    # Run the circuit and collect samples
    samples = circuit()
    
    # Convert samples to bitstrings and count occurrences
    counts = defaultdict(int)
    for sample in samples:
        # Convert array of 0s and 1s to a bitstring
        bitstring = ''.join(str(int(bit)) for bit in sample[::-1])  # Reverse to match Qiskit's ordering
        counts[bitstring] += 1
    
    # Normalize to get probabilities
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
