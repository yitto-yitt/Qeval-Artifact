# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml

dev = qml.device("default.qubit", wires=9)

@qml.qnode(dev)
def _circuit(a, b):
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    for i in range(3):
        if a_bin[2-i] == '1':
            qml.PauliX(wires=i)
        if b_bin[2-i] == '1':
            qml.PauliX(wires=i+3)
    for i in range(3):
        qml.Toffoli(wires=[i, i+3, i+6])
    return qml.probs(wires=[8, 7, 6])

def and_gate(a, b):
    probs = _circuit(a, b)
    result = {}
    for i, p in enumerate(probs):
        if p > 1e-9:
            result[format(i, '03b')] = float(p)
    return result
