# EVAL_META: task_id=92, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np

def calculate_stabilizer_state_info():
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0, 1])
    
    probs = circuit()
    
    # Convert to dictionary format matching Qiskit's probabilities_dict
    prob_dict = {}
    for i, prob in enumerate(probs):
        key = format(i, '02b')  # Convert index to 2-bit binary string
        if prob > 1e-10:  # Only include non-negligible probabilities
            prob_dict[key] = float(prob)
    
    return prob_dict
