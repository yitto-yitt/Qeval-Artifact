# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    dev = qml.device("default.qubit", wires=8)

    @qml.qnode(dev)
    def circuit():
        bits = format(int(a), "08b")
        for i in range(8):
            if bits[7 - i] == "0":
                qml.PauliX(wires=i)
        return qml.probs(wires=[7, 6, 5, 4, 3, 2, 1, 0])

    probs = circuit()
    return {format(i, "08b"): float(p) for i, p in enumerate(probs) if p > 1e-12}
