# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    dev = qml.device("default.qubit", wires=8)

    @qml.qnode(dev)
    def circuit():
        c = a ^ b
        for i in range(8):
            if (c >> i) & 1:
                qml.PauliX(wires=i)
        return qml.probs(wires=[7, 6, 5, 4, 3, 2, 1, 0])

    probs = circuit()
    return {f"{i:08b}": float(prob) for i, prob in enumerate(probs) if prob > 0}
