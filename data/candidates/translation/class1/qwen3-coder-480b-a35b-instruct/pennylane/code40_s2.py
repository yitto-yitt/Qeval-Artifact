# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3, seed=42)
    
    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(desired_vector, wires=[0, 1, 2])
        return qml.probs(wires=[0, 1, 2])
    
    probs = circuit()
    outcomes = {}
    for i in range(len(probs)):
        bitstring = format(i, '03b')
        outcomes[bitstring] = probs[i]
    return outcomes
