# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def dj_algorithm(oracle):
    n = int(np.log2(oracle.shape[0]))
    dev = qml.device("default.qubit", wires=n)
    
    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n-1)
        for w in range(n):
            qml.Hadamard(wires=w)
        qml.QubitUnitary(oracle, wires=range(n))
        for w in range(n):
            qml.Hadamard(wires=w)
        return qml.probs(wires=range(n-1))
    
    probs = circuit()
    return {format(i, '0{}b'.format(n-1)): probs[i] for i in range(len(probs))}
