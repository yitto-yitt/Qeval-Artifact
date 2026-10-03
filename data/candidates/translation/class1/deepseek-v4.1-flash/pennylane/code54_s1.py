# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml

def and_gate(a, b):
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    a_wires = [0, 1, 2]
    b_wires = [3, 4, 5]
    ancilla_wires = [6, 7, 8]
    dev = qml.device("default.qubit", wires=9)

    @qml.qnode(dev)
    def circuit():
        for i in range(3):
            if a_bits[2 - i] == '1':
                qml.PauliX(wires=a_wires[i])
            if b_bits[2 - i] == '1':
                qml.PauliX(wires=b_wires[i])
        for i in range(3):
            qml.Toffoli(wires=[a_wires[i], b_wires[i], ancilla_wires[i]])
        return qml.probs(wires=[ancilla_wires[2], ancilla_wires[1], ancilla_wires[0]])

    probs = circuit()
    return {format(i, '03b'): float(p) for i, p in enumerate(probs) if p > 1e-12}
