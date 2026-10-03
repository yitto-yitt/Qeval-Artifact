# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def not_gate(a):
    bits = format(a, "08b")
    device = qml.device("default.qubit", wires=8)

    @qml.set_shots(shots=1024)
    @qml.qnode(device)
    def circuit():
        for i in range(8):
            if bits[7 - i] == "0":
                qml.PauliX(wires=i)
        return qml.sample(wires=list(range(7, -1, -1)))

    samples = np.asarray(circuit())
    counts = {}
    for sample in samples:
        key = "".join(str(int(bit)) for bit in sample)
        counts[key] = counts.get(key, 0) + 1
    total = len(samples)
    return {key: value / total for key, value in counts.items()}
