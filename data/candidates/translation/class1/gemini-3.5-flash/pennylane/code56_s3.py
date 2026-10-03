# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    dev = qml.device("default.qubit", wires=8)

    @qml.qnode(dev)
    def circuit():
        a_bin = format(a, "08b")
        for i in range(8):
            if a_bin[7-i] == "0":
                qml.X(i)
        return qml.probs(wires=range(8))

    probs = circuit()
    result = {}
    for idx, prob in enumerate(probs):
        if prob > 1e-6:
            key = "".join(str((idx >> i) & 1) for i in range(8))
            result[key] = float(prob)
    return result
