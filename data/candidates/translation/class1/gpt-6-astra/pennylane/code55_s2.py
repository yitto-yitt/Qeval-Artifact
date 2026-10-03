# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml

def or_gate(a, b):
    a = format(a, "03b")
    b = format(b, "03b")
    device = qml.device("default.qubit", wires=9)

    @qml.set_shots(shots=1024)
    @qml.qnode(device)
    def circuit():
        for i in range(3):
            if a[2 - i] == "0":
                qml.PauliX(wires=i)
            if b[2 - i] == "0":
                qml.PauliX(wires=3 + i)
        for i in range(3):
            qml.Toffoli(wires=[i, 3 + i, 6 + i])
        for i in range(3):
            qml.PauliX(wires=6 + i)
        return qml.counts(wires=[8, 7, 6])

    counts = circuit()
    total = sum(counts.values())
    return {str(key): int(value) / total for key, value in counts.items()}
