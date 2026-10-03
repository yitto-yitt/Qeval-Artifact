# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml

def and_gate(a, b):
    qa = [0, 1, 2]
    qb = [3, 4, 5]
    anc = [6, 7, 8]

    dev = qml.device("default.qubit", wires=9, shots=1024)

    a_str = format(a, "03b")
    b_str = format(b, "03b")

    @qml.qnode(dev)
    def circuit():
        for i in range(3):
            if a_str[2 - i] == "1":
                qml.PauliX(wires=qa[i])
            if b_str[2 - i] == "1":
                qml.PauliX(wires=qb[i])

        for i in range(3):
            qml.Toffoli(wires=[qa[i], qb[i], anc[i]])

        return qml.counts(wires=[anc[2], anc[1], anc[0]])

    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items() if value > 0}
