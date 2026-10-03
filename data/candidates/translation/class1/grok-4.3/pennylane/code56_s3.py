# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    dev = qml.device("default.qubit", wires=8)
    @qml.qnode(dev)
    def circuit():
        a_bin = format(a, "08b")
        for i in range(8):
            if a_bin[7 - i] == "0":
                qml.PauliX(wires=i)
        return qml.probs(wires=range(8))
    probs_array = circuit()
    result = {}
    for k in range(256):
        if probs_array[k] > 1e-10:
            bin_str = format(k, "08b")
            key = bin_str[::-1]
            result[key] = float(probs_array[k])
    return result
