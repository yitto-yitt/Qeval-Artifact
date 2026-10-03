# EVAL_META: task_id=31, framework=pennylane, class=1
import pennylane as qml
from typing import Dict

def sampler_qiskit():
    dev = qml.device("default.qubit", wires=2, seed=42)
    
    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0, 1])
    
    probs = bell_circuit()
    
    # Convert probabilities to bitstring format
    result = {}
    for i, prob in enumerate(probs):
        bitstring = format(i, '02b')  # Convert index to 2-bit binary string
        if prob > 0:
            result[bitstring] = prob
    
    return result
