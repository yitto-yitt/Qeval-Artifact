# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def init_random_3qubit(desired_vector):
    desired_vector = np.array(desired_vector, dtype=complex)
    norm = np.linalg.norm(desired_vector)
    if norm > 0:
        desired_vector = desired_vector / norm
        
    dev = qml.device("default.qubit", wires=3)
    
    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(desired_vector, wires=[0, 1, 2])
        return qml.probs(wires=[0, 1, 2])
        
    probs = circuit()
    
    prob_dict = {}
    for i, p in enumerate(probs):
        if p > 1e-9:
            prob_dict[format(i, '03b')] = float(p)
            
    return prob_dict
