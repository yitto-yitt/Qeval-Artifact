# EVAL_META: task_id=65, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QCircuit, H, SWAP, CU, U1

def QFT(n):
    circuit = QCircuit()

    def swap_registers(circuit, n):
        for qubit in range(n // 2):
            circuit << SWAP(qubit, n - qubit - 1)
        return circuit

    def qft_rotations(circuit, n):
        if n == 0:
            return circuit
        n -= 1
        circuit << H(n)
        for qubit in range(n):
            theta = pi / (2 ** (n - qubit))
            circuit << CU(U1(theta), qubit, n)
        qft_rotations(circuit, n)
        return circuit

    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
