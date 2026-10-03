# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    dev = qml.device('default.qubit', wires=8, shots=None)
    a_bin = format(a, "08b")

    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if a_bin[7 - i] == "0":
                qml.PauliX(wires=i)
        return qml.probs(wires=range(8))

    probs = circuit()
    return {format(i, "08b")[::-1]: float(probs[i]) for i in range(256) if probs[i] > 0}
