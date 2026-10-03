# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml

def or_gate(a, b):
    dev = qml.device("default.qubit", wires=9)
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')

    @qml.qnode(dev)
    def circuit():
        for i in range(3):
            if a_bits[2-i] == '0':
                qml.PauliX(wires=i)
            if b_bits[2-i] == '0':
                qml.PauliX(wires=3+i)
        for i in range(3):
            qml.Toffoli(wires=[i, 3+i, 6+i])
        for i in range(3):
            qml.PauliX(wires=6+i)
        return qml.probs(wires=[6, 7, 8])

    probs = circuit()
    result = {}
    for idx, p in enumerate(probs):
        if p > 1e-12:
            key = format(idx, '03b')
            result[key] = float(p)
    return result
