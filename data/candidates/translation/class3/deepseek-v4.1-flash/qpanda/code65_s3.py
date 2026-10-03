# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import *
from math import pi

def QFT(n):
    circuit = QCircuit()
    qubits = [Qubit(i) for i in range(n)]
    def qft_rotations(n):
        if n == 0:
            return
        n -= 1
        circuit << H(qubits[n])
        for qubit in range(n):
            circuit << CR(qubits[qubit], qubits[n], pi / 2**(n - qubit))
        qft_rotations(n)
    def swap_registers(n):
        for qubit in range(n // 2):
            circuit << SWAP(qubits[qubit], qubits[n - qubit - 1])
    qft_rotations(n)
    swap_registers(n)
    return circuit
