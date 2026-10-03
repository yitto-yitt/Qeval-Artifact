# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np

def init_random_3qubit(desired_vector):
    dev = qml.device('default.qubit', wires=3, shots=1000)

    @qml.qnode(dev)
    def circuit():
        qml.QubitStateVector(desired_vector, wires=range(3))
        return qml.probs(wires=range(3))

    probs = circuit()
    basis_states = [format(i, '03b') for i in range(8)]
    prob_dict = {basis_states[i]: float(probs[i]) for i in range(8)}
    
    # Convert to counts to match Qiskit's output format, then back to probabilities
    counts = {k: int(v * 1000) for k, v in prob_dict.items()}
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
