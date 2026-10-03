# EVAL_META: task_id=1, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np

def run_bell_state_simulator():
    dev = qml.device("default.qubit", wires=2, shots=1000)
    
    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])
    
    samples = bell_circuit()
    
    # Convert samples to bitstrings and count occurrences
    bitstring_counts = {}
    for sample in samples:
        bitstring = ''.join(map(str, sample.astype(int)))
        bitstring_counts[bitstring] = bitstring_counts.get(bitstring, 0) + 1
    
    total = len(samples)
    return {key: value / total for key, value in bitstring_counts.items()}
