# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml

def or_gate(a, b):
    wires_a = [0, 1, 2]
    wires_b = [3, 4, 5]
    anc_wires = [8, 7, 6]
    dev = qml.device("default.qubit", wires=9, shots=1024)

    @qml.qnode(dev)
    def circuit():
        a_str = format(a, "03b")
        b_str = format(b, "03b")
        for i in range(3):
            if a_str[2 - i] == "0":
                qml.PauliX(wires=wires_a[i])
            if b_str[2 - i] == "0":
                qml.PauliX(wires=wires_b[i])
        for i in range(3):
            qml.Toffoli(wires=[wires_a[i], wires_b[i], anc_wires[i]])
        for i in range(3):
            qml.PauliX(wires=anc_wires[i])
        return qml.counts(wires=[6, 7, 8])

    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
