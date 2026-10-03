# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    dev = qml.device("default.qubit", wires=8)
    a = format(a, "08b")

    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if a[7 - i] == "0":
                qml.PauliX(wires=i)
        return qml.probs(wires=list(reversed(range(8))))

    probs = circuit()
    result = {}
    for i, p in enumerate(probs):
        p = float(p)
        if p > 1e-12:
            result[format(i, "08b")] = p

    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
