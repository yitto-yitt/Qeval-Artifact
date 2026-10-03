# EVAL_META: task_id=65, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QCircuit, H, SWAP, CR

def QFT(n):
    circuit = QCircuit()

    def swap_registers(circ, num_qubits):
        for qubit in range(num_qubits // 2):
            circ << SWAP(qubit, num_qubits - qubit - 1)
        return circ

    def qft_rotations(circ, num_qubits):
        if num_qubits == 0:
            return circ
        num_qubits -= 1
        circ << H(num_qubits)
        for qubit in range(num_qubits):
            circ << CR(qubit, num_qubits, pi / (2 ** (num_qubits - qubit)))
        qft_rotations(circ, num_qubits)
        return circ

    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
