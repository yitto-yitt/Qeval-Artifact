# EVAL_META: task_id=40, framework=pennylane, class=1
import numpy as np
import pennylane as qml

def init_random_3qubit(desired_vector):
    vec = np.array(desired_vector, dtype=complex)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
        
    dev = qml.device("default.qubit", wires=3)
    
    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(vec, wires=[2, 1, 0])
        return qml.probs(wires=[2, 1, 0])
    
    probs = circuit()
    return {f"{i:03b}": float(p) for i, p in enumerate(probs)}
