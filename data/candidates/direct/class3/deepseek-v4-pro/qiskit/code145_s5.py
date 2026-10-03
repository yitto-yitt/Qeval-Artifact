# EVAL_META: task_id=145, framework=qiskit, class=3
from qiskit import QuantumCircuit
from math import pi

def qft_inverse(n):
    qc = QuantumCircuit(n)
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)
    for qubit in reversed(range(n)):
        for k in reversed(range(qubit + 1, n)):
            qc.cp(-pi / 2 ** (k - qubit), k, qubit)
        qc.h(qubit)
    return qc
