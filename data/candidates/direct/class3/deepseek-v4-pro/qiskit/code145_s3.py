# EVAL_META: task_id=145, framework=qiskit, class=3
from math import pi
from qiskit import QuantumCircuit

def qft_inverse(n):
    qc = QuantumCircuit(n)

    # Undo qubit reversal swaps from the standard QFT
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)

    # Apply inverse rotations and inverse Hadamards in reverse order
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            qc.cp(-pi / (2 ** (j - i)), j, i)
        qc.h(i)

    return qc
