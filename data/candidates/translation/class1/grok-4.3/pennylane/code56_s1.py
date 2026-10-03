# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    dev = qml.device("default.qubit", wires=8)
    @qml.qnode(dev)
    def circuit():
        a_bin = format(a, "08b")
        for i in range(8):
            if a_bin[7 - i] == "0":
                qml.X(i)
        return qml.probs(wires=range(8))
    probs = circuit()
    n = len(probs)
    result = {}
    for i in range(n):
        if probs[i] > 1e-10:
            key = format(i, "08b")
            result[key] = float(probs[i])
    return result
