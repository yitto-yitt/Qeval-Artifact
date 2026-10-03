# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml
import numpy as np


def xor_gate(a, b):
    num_wires = 8
    dev = qml.device("default.qubit", wires=num_wires, shots=1024)

    @qml.qnode(dev)
    def circuit():
        # XOR(8, a): flip qubit i when bit i of a is 1
        for i in range(num_wires):
            if (a >> i) & 1:
                qml.PauliX(wires=i)
        # XOR(8, b): flip qubit i when bit i of b is 1
        for i in range(num_wires):
            if (b >> i) & 1:
                qml.PauliX(wires=i)
        return qml.sample(wires=list(range(num_wires)))

    samples = np.asarray(circuit())
    samples = samples.reshape(-1, num_wires)

    counts = {}
    for row in samples:
        # Qiskit convention: leftmost character is qubit 7, rightmost is qubit 0
        bitstring = "".join(str(int(row[k])) for k in range(num_wires - 1, -1, -1))
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {key: val / total for key, val in counts.items()}
