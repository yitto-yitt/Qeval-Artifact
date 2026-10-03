# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    dev = qml.device("default.qubit", wires=8)

    @qml.set_shots(shots=1024)
    @qml.qnode(dev)
    def circuit():
        for value in (a, b):
            for wire in range(8):
                if (value >> wire) & 1:
                    qml.PauliX(wires=wire)
        return qml.counts(wires=list(range(7, -1, -1)))

    counts = circuit()
    total = sum(counts.values())
    return {key: float(value / total) for key, value in counts.items()}
