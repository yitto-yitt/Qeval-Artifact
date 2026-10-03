# EVAL_META: task_id=145, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit


def qft_inverse(n):
    qc = QuantumCircuit(n)

    # Swap qubits to reverse order (undo the swaps at the end of QFT)
    for i in range(n // 2):
        qc.swap(i, n - i - 1)

    # Apply inverse QFT rotations in reverse order
    for j in range(n - 1, -1, -1):
        for k in range(n - 1, j, -1):
            angle = -2 * np.pi / (2 ** (k - j + 1))
            qc.cp(angle, k, j)
        qc.h(j)

    return qc
