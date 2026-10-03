# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def xor_gate(a, b):
    n = 8
    dev = qml.device("default.qubit", wires=n)
    
    @qml.qnode(dev)
    def circuit():
        for i in range(n):
            if (a >> i) & 1:
                qml.PauliX(wires=i)
        for i in range(n):
            if (b >> i) & 1:
                qml.PauliX(wires=i)
        return qml.probs(wires=list(range(n-1, -1, -1)))
    
    probs = circuit()
    index = int(np.argmax(probs))
    return {format(index, '08b'): 1.0}
