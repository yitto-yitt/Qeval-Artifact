# EVAL_META: task_id=145, framework=qiskit, class=3
from math import pi
from qiskit import QuantumCircuit


def qft_inverse(n):
    circuit = QuantumCircuit(n, name="IQFT")

    for qubit in range(n // 2):
        circuit.swap(qubit, n - qubit - 1)

    for target in range(n):
        for control in range(target):
            circuit.cp(-pi / (2 ** (target - control)), control, target)
        circuit.h(target)

    return circuit
