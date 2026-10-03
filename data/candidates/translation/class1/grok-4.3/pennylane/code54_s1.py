# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml

def and_gate(a, b):
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    dev = qml.device("default.qubit", wires=9, shots=1024)
    @qml.qnode(dev)
    def circuit():
        for i in range(3):
            if a_bin[2 - i] == '1':
                qml.PauliX(wires=i)
            if b_bin[2 - i] == '1':
                qml.PauliX(wires=3 + i)
        for i in range(3):
            qml.Toffoli(wires=[i, 3 + i, 6 + i])
        return qml.counts(wires=[8, 7, 6])
    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
