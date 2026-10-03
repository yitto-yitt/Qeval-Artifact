# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml

def and_gate(a, b):
    dev = qml.device("default.qubit", wires=9)
    a = format(a, '03b')
    b = format(b, '03b')

    @qml.qnode(dev)
    def circuit():
        for i in range(3):
            if a[2-i] == '1':
                qml.PauliX(wires=i)
            if b[2-i] == '1':
                qml.PauliX(wires=3+i)
        for i in range(3):
            qml.Toffoli(wires=[i, 3+i, 6+i])
        return qml.probs(wires=[6, 7, 8])

    probs = circuit()
    result = {}
    for idx, p in enumerate(probs):
        if p > 1e-12:
            key = format(idx, '03b')
            result[key] = float(p)
    return result
