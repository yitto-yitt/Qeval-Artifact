# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3)
    
    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(desired_vector, wires=[0, 1, 2])
        return qml.probs(wires=[0, 1, 2])
        
    probs = circuit()
    
    result = {}
    for i, p in enumerate(probs):
        if p > 1e-10:
            result[f"{i:03b}"] = float(p)
            
    return result
