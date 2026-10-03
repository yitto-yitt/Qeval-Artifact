# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, SWAP, P
from numpy import pi

def QFT(n):
    circuit = QCircuit(n)

    def qft_rotations(circuit, m):
        if m == 0:
            return circuit
        m -= 1
        circuit << H(m)
        for qubit in range(m):
            circuit << P(m, pi / 2 ** (m - qubit)).control(qubit)
        qft_rotations(circuit, m)

    def swap_registers(circuit, m):
        for qubit in range(m // 2):
            circuit << SWAP(qubit, m - qubit - 1)
        return circuit

    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
