# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    dev = qml.device('default.qubit', wires=8)
    @qml.qnode(dev)
    def circuit():
        for j in range(8):
            if (a & (1 << j)):
                qml.PauliX(wires=7 - j)
            if (b & (1 << j)):
                qml.PauliX(wires=7 - j)
        return qml.probs(wires=range(8))
    probs = circuit()
    result = {}
    for i in range(256):
        if probs[i] > 1e-10:
            key = f'{i:08b}'
            result[key] = float(probs[i])
    return result
