# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml
from collections import defaultdict

def dj_algorithm(oracle):
    n = len(oracle.wires)
    
    dev = qml.device('default.qubit', wires=n, shots=1000)
    
    @qml.qnode(dev)
    def circuit():
        # Flip the last qubit to |1>
        qml.PauliX(wires=n-1)
        
        # Apply Hadamard to all qubits
        for i in range(n):
            qml.Hadamard(wires=i)
        
        # Apply the oracle
        oracle(wires=range(n))
        
        # Apply Hadamard to all qubits again
        for i in range(n):
            qml.Hadamard(wires=i)
        
        # Measure the first n-1 qubits
        return [qml.measure(wires=i) for i in range(n-1)]
    
    # Run the circuit
    results = circuit()
    
    # Convert results to bitstrings and count frequencies
    counts = defaultdict(int)
    if dev.shots is not None:
        for sample in dev.samples:
            # Convert array of 0s and 1s to string, reversing to match Qiskit's convention
            bitstring = ''.join(str(int(bit)) for bit in reversed(sample[:n-1]))
            counts[bitstring] += 1
    else:
        # For exact probabilities when shots=None
        probs = dev.probability()
        for i, prob in enumerate(probs):
            if prob > 1e-10:  # Only include non-zero probabilities
                # Convert index to binary string
                bitstring = format(i, f'0{n-1}b')
                counts[bitstring] = prob
    
    # Normalize to get probabilities
    total = sum(counts.values())
    if total > 0:
        normalized_counts = {key: value/total for key, value in counts.items()}
    else:
        normalized_counts = counts
        
    return normalized_counts
