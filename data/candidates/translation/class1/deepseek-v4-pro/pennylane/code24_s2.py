# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml
import numpy as np


def dj_algorithm(oracle):
    if hasattr(oracle, "num_qubits"):
        n = int(oracle.num_qubits)
    elif hasattr(oracle, "num_wires"):
        n = int(oracle.num_wires)
    elif hasattr(oracle, "wires"):
        n = len(oracle.wires)
    else:
        raise ValueError("Cannot infer number of qubits from oracle")

    m = n - 1
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n - 1)
        for wire in range(n):
            qml.Hadamard(wires=wire)

        if callable(oracle):
            oracle(list(range(n)))
        else:
            qml.apply(oracle)

        for wire in range(n):
            qml.Hadamard(wires=wire)

        return qml.probs(wires=list(range(m)))

    probs = circuit()

    if m == 0:
        return {"": 1.0}

    return {
        format(i, f"0{m}b"): float(p)
        for i, p in enumerate(probs)
        if not np.isclose(p, 0.0)
    }
