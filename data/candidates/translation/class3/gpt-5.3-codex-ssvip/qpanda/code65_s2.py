# EVAL_META: task_id=65, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QCircuit, H, SWAP, CU, P

def QFT(n):
    circuit = QCircuit()

    def swap_registers(circ, n_qubits):
        for qubit in range(n_qubits // 2):
            circ << SWAP(qubit, n_qubits - qubit - 1)
        return circ

    def qft_rotations(circ, m):
        if m == 0:
            return circ
        m -= 1
        circ << H(m)
        for qubit in range(m):
            angle = pi / (2 ** (m - qubit))
            circ << CU(P(angle), qubit, m)
        qft_rotations(circ, m)
        return circ

    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
