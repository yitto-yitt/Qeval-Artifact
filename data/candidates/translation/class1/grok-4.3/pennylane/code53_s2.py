# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    n = 8
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        for k in range(n):
            if (a >> k) & 1:
                qml.PauliX(wires=n - 1 - k)
        for k in range(n):
            if (b >> k) & 1:
                qml.PauliX(wires=n - 1 - k)
        return qml.probs(wires=range(n))

    probs = circuit()
    result = {}
    for i, p in enumerate(probs):
        if p > 1e-10:
            bin_str = format(i, "08b")
            result[bin_str] = float(p)
    return result
