# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def not_gate(a):
    dev = qml.device("default.qubit", wires=8)
    
    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if ((a >> i) & 1) == 0:
                qml.PauliX(wires=i)
        return qml.probs(wires=[7, 6, 5, 4, 3, 2, 1, 0])
    
    probs = circuit()
    idx = int(np.argmax(probs))
    bitstring = format(idx, "08b")
    return {bitstring: float(probs[idx])}
