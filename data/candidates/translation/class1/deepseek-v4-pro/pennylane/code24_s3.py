# EVAL_META: task_id=24, framework=pennylane, class=1
import math
import pennylane as qml
from pennylane import numpy as np


def dj_algorithm(oracle):
    if hasattr(oracle, "wires") and not callable(oracle):
        n = len(oracle.wires)

        def apply_oracle():
            qml.apply(oracle)

    elif callable(oracle):
        with qml.tape.QuantumTape() as tape:
            oracle()
        n = len(tape.wires)

        def apply_oracle():
            oracle()

    else:
        shape = np.shape(oracle)
        n = int(round(math.log2(shape[0])))

        def apply_oracle():
            qml.QubitUnitary(oracle, wires=range(n))

    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n - 1)
        for i in range(n):
            qml.Hadamard(wires=i)
        apply_oracle()
        for i in range(n):
            qml.Hadamard(wires=i)
        return qml.probs(wires=range(n - 2, -1, -1))

    probs = circuit()
    keys = [format(i, f"0{n - 1}b") for i in range(2 ** (n - 1))]
    return {key: float(p) for key, p in zip(keys, probs) if p > 1e-15}
