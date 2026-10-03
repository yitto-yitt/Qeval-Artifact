# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    a_bin = format(a, "08b")
    dev = qml.device("default.qubit", wires=8)
    @qml.qnode(dev)
    def circuit():
        for j in range(8):
            if a_bin[j] == "0":
                qml.PauliX(wires=j)
        return qml.probs(wires=range(8))
    probs = circuit()
    prob_dict = {}
    for i in range(256):
        if probs[i] > 1e-6:
            key = format(i, "08b")
            prob_dict[key] = float(probs[i])
    return prob_dict
