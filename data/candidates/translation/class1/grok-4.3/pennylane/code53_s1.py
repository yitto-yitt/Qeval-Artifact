# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    n = 8
    dev = qml.device("default.qubit", wires=n)
    @qml.qnode(dev)
    def circuit():
        for i in range(n):
            if (a & (1 << i)) != 0:
                qml.X(wires=i)
        for i in range(n):
            if (b & (1 << i)) != 0:
                qml.X(wires=i)
        return qml.probs(wires=range(n))
    probs = circuit()
    result = {}
    for i in range(2**n):
        if probs[i] > 1e-6:
            key = format(i, f'0{n}b')
            result[key] = float(probs[i])
    return result
