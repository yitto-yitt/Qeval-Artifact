# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CR, SWAP
from numpy import pi

def QFT(n):
    circuit = QCircuit()

    def qft_rotations(k):
        if k == 0:
            return
        k -= 1
        circuit << H(k)
        for qubit in range(k):
            circuit << CR(qubit, k, pi / 2 ** (k - qubit))
        qft_rotations(k)

    def swap_registers(k):
        for qubit in range(k // 2):
            circuit << SWAP(qubit, k - qubit - 1)

    qft_rotations(n)
    swap_registers(n)
    return circuit
