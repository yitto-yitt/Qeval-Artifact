# EVAL_META: task_id=77, framework=pennylane, class=1
import math
import pennylane as qml
from pennylane import numpy as np

def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))
    
    dev = qml.device("default.qubit", wires=num_qubits)
    
    @qml.qnode(dev)
    def circuit():
        qml.AmplitudeEmbedding(features=amplitudes, wires=range(num_qubits), normalize=True)
        return qml.probs(wires=range(num_qubits))
    
    # Execute the circuit to ensure it's properly defined
    circuit()
    
    return circuit.func
