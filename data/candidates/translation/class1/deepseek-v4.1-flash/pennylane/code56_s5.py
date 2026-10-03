# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    n = 8
    bits = format(a, "08b")
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        for i in range(n):
            if bits[7 - i] == "0":
                qml.PauliX(wires=i)
        return qml.probs(wires=range(n))

    probs = circuit()
    return {format(i, "08b"): float(probs[i]) for i in range(2 ** n)}
