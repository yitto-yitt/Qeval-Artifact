# EVAL_META: task_id=65, framework=qiskit, class=3

from math import pi
from qiskit import QuantumCircuit


def QFT(n):
    circuit = QuantumCircuit(n, name="QFT")

    for target in reversed(range(n)):
        circuit.h(target)
        for control in reversed(range(target)):
            circuit.cp(pi / (2 ** (target - control)), control, target)

    for qubit in range(n // 2):
        circuit.swap(qubit, n - qubit - 1)

    return circuit
