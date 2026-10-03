# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def not_gate(a):
    dev = qml.device("default.qubit", wires=8)
    
    @qml.qnode(dev)
    def circuit():
        a_str = format(a, "08b")
        for i in range(8):
            if a_str[7-i] == "0":
                qml.PauliX(wires=i)
        return qml.probs(wires=range(8))
    
    probs = circuit()
    idx = int(np.argmax(probs))
    bitstring = format(idx, '08b')
    return {bitstring: 1.0}
