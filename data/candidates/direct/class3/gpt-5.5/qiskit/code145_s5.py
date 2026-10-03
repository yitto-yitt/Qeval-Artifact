# EVAL_META: task_id=145, framework=qiskit, class=3
from math import pi
from qiskit import QuantumCircuit


def qft_inverse(n):
    circuit = QuantumCircuit(n)

    for i in range(n // 2):
        circuit.swap(i, n - i - 1)

    for j in range(n):
        for m in range(j):
            circuit.cp(-pi / (2 ** (j - m)), m, j)
        circuit.h(j)

    return circuit
