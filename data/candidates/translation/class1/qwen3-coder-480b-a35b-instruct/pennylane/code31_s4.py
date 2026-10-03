# EVAL_META: task_id=31, framework=pennylane, class=1
import pennylane as qml
from typing import Dict

def sampler_qiskit():
    dev = qml.device("default.qubit", wires=2, seed=42)
    
    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])
    
    samples = bell_circuit()
    
    # Count the occurrences of each bitstring
    counts = {}
    for sample in samples:
        bitstring = ''.join(map(str, sample))
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    total = len(samples)
    return {key: value / total for key, value in counts.items()}
