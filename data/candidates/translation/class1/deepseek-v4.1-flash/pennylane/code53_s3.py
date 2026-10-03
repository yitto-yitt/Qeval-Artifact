# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def xor_gate(a, b):
    x = a ^ b
    dev = qml.device("default.qubit", wires=8)

    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if (x >> (7 - i)) & 1:
                qml.PauliX(wires=i)
        return qml.probs(wires=list(range(8)))

    probs = circuit()
    index = int(np.argmax(probs))
    bitstring = format(index, '08b')
    return {bitstring: 1.0}
