# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml

def and_gate(a, b):
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    dev = qml.device('default.qubit', wires=9)

    @qml.qnode(dev)
    def circuit():
        for i in range(3):
            if a_bits[2 - i] == '1':
                qml.PauliX(wires=i)
            if b_bits[2 - i] == '1':
                qml.PauliX(wires=3 + i)
        for i in range(3):
            qml.Toffoli(wires=[i, 3 + i, 6 + i])
        return qml.probs(wires=[8, 7, 6])

    probs = circuit()
    return {f"{idx:03b}": float(prob) for idx, prob in enumerate(probs) if prob > 0}
