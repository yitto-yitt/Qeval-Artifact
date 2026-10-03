# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    wires = list(range(7, -1, -1))
    dev = qml.device("default.qubit", wires=8, shots=1024)

    @qml.qnode(dev)
    def circuit():
        x = a ^ b
        for i in range(8):
            if (x >> i) & 1:
                qml.PauliX(wires=i)
        return qml.counts(wires=wires)

    counts = circuit()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
