# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    dev = qml.device("default.qubit", wires=8)
    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if (a >> i) & 1:
                qml.PauliX(wires=i)
        for i in range(8):
            if (b >> i) & 1:
                qml.PauliX(wires=i)
        return qml.probs(wires=range(8))
    probs = circuit()
    bitstrings = [f"{k:08b}" for k in range(256)]
    return {bitstrings[k]: float(p) for k, p in enumerate(probs) if p > 1e-8}
