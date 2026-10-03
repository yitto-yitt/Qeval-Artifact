# EVAL_META: task_id=78, framework=qiskit, class=3

from math import pi
from qiskit import QuantumCircuit


def qft_no_swaps(num_qubits):
    """Return an inverse QFT circuit without swap gates."""
    qc = QuantumCircuit(num_qubits)

    for j in range(num_qubits):
        for m in range(j):
            qc.cp(-pi / (2 ** (j - m)), m, j)
        qc.h(j)

    return qc
