# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3, seed=42)
    
    @qml.qnode(dev)
    def circuit():
        qml.StatePreparation(desired_vector, wires=[0, 1, 2])
        return qml.probs(wires=[0, 1, 2])
    
    probs = circuit()
    num_outcomes = len(probs)
    
    # Create bitstring keys and convert probabilities to dictionary
    prob_dict = {}
    for i in range(num_outcomes):
        bitstring = format(i, f'03b')
        prob_dict[bitstring] = probs[i]
    
    return prob_dict
