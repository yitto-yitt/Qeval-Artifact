# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit
from math import pi

def QFT(n):
    circuit = QuantumCircuit(n)

    def swap_registers(circuit, n):
        for qubit in range(n // 2):
            circuit.swap(qubit, n - qubit - 1)
        return circuit

    def qft_rotations(circuit, n):
        if n == 0:
            return circuit
        n -= 1
        circuit.h(n)
        for qubit in range(n):
            circuit.cp(pi / 2 ** (n - qubit), qubit, n)
        qft_rotations(circuit, n)

    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
