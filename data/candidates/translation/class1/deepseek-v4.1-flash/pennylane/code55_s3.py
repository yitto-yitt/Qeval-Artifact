# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml

def or_gate(a, b):
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    dev = qml.device("default.qubit", wires=9)
    @qml.qnode(dev)
    def circuit():
        for i in range(3):
            if a_str[2-i] == '0':
                qml.PauliX(wires=i)
            if b_str[2-i] == '0':
                qml.PauliX(wires=3+i)
        for i in range(3):
            qml.Toffoli(wires=[i, 3+i, 6+i])
        for i in range(3):
            qml.PauliX(wires=6+i)
        return qml.probs(wires=[6, 7, 8])
    probs = circuit()
    return {format(idx, '03b'): float(prob) for idx, prob in enumerate(probs) if prob > 1e-10}
