# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, SWAP, P
from numpy import pi

def QFT(n):
    circuit = QCircuit(n)
    def swap_registers(circuit, n):
        for qubit in range(n//2):
            circuit << SWAP(qubit, n-qubit-1)
        return circuit
    def qft_rotations(circuit, n):
        if n == 0:
            return circuit
        n -= 1
        circuit << H(n)
        for qubit in range(n):
            circuit << P(n, pi/2**(n-qubit)).control(qubit)
        qft_rotations(circuit, n)

    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
