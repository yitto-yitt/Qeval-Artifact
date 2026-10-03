# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml

def or_gate(a, b):
    a_wires = [0, 1, 2]
    b_wires = [3, 4, 5]
    anc_wires = [6, 7, 8]

    dev = qml.device("default.qubit", wires=9)

    @qml.qnode(dev)
    def circuit():
        a_bits = f"{a:03b}"
        b_bits = f"{b:03b}"

        for i in range(3):
            if a_bits[2 - i] == "0":
                qml.PauliX(wires=a_wires[i])
            if b_bits[2 - i] == "0":
                qml.PauliX(wires=b_wires[i])

        for i in range(3):
            qml.Toffoli(wires=[a_wires[i], b_wires[i], anc_wires[i]])

        for i in range(3):
            qml.PauliX(wires=anc_wires[i])

        return qml.probs(wires=anc_wires)

    probs = circuit()
    return {f"{i:03b}": float(probs[i]) for i in range(8) if probs[i] > 0.5}
