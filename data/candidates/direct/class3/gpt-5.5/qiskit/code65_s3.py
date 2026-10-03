# EVAL_META: task_id=65, framework=qiskit, class=3
from math import pi
from qiskit import QuantumCircuit


def QFT(n):
    qc = QuantumCircuit(n, name="QFT")

    for target in range(n - 1, -1, -1):
        qc.h(target)
        for control in range(target):
            qc.cp(pi / (2 ** (target - control)), control, target)

    for i in range(n // 2):
        qc.swap(i, n - i - 1)

    return qc
