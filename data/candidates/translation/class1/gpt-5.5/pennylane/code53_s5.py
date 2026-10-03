# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def xor_gate(a, b):
    dev = qml.device("default.qubit", wires=8)

    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if (int(a) >> i) & 1:
                qml.PauliX(wires=i)
        for i in range(8):
            if (int(b) >> i) & 1:
                qml.PauliX(wires=i)
        return qml.probs(wires=list(range(7, -1, -1)))

    probs = circuit()
    return {format(i, "08b"): float(p) for i, p in enumerate(probs) if not np.isclose(p, 0.0)}
