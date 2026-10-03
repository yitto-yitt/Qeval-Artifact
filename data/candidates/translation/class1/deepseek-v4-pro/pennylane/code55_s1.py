# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml

def or_gate(a, b):
    qr_a = [0, 1, 2]
    qr_b = [3, 4, 5]
    ancillary = [6, 7, 8]

    dev = qml.device("default.qubit", wires=9)

    @qml.qnode(dev)
    def circuit():
        a_bin = format(a, "03b")
        b_bin = format(b, "03b")

        for i in range(3):
            if a_bin[2 - i] == "0":
                qml.X(wires=qr_a[i])
            if b_bin[2 - i] == "0":
                qml.X(wires=qr_b[i])

        for i in range(3):
            qml.Toffoli(wires=[qr_a[i], qr_b[i], ancillary[i]])

        for i in range(3):
            qml.X(wires=ancillary[i])

        return qml.probs(wires=[ancillary[2], ancillary[1], ancillary[0]])

    probs = circuit()
    return {format(i, "03b"): float(probs[i]) for i in range(len(probs)) if probs[i] > 0}
