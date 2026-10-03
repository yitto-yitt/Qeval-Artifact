# EVAL_META: task_id=65, framework=qiskit, class=3
from math import pi
from qiskit import QuantumCircuit


def QFT(n):
    """Return an n-qubit Quantum Fourier Transform circuit."""
    qc = QuantumCircuit(n)

    for i in range(n - 1, -1, -1):
        qc.h(i)
        for j in range(i):
            qc.cp(pi / (2 ** (i - j)), j, i)

    for i in range(n // 2):
        qc.swap(i, n - 1 - i)

    return qc
