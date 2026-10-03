# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml

def init_random_3qubit(desired_vector):
    dev = qml.device('default.qubit', wires=3)
    
    @qml.qnode(dev)
    def circuit(state):
        qml.StatePrep(state, wires=[0, 1, 2])
        return qml.probs(wires=[0, 1, 2])
    
    probs = circuit(desired_vector)
    return {f"{i:03b}": float(probs[i]) for i in range(8)}
