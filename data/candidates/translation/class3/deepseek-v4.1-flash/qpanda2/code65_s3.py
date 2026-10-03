# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
from math import pi

machine = CPUQVM()
machine.init_qvm()


def QFT(n):
    qubits = machine.qAlloc_many(n)
    circuit = QCircuit()

    def qft_rotations(circuit, n):
        if n == 0:
            return circuit
        n -= 1
        circuit << H(qubits[n])
        for qubit in range(n):
            circuit << CR(qubits[qubit], qubits[n], pi / 2 ** (n - qubit))
        return qft_rotations(circuit, n)

    def swap_registers(circuit, n):
        for qubit in range(n // 2):
            circuit << SWAP(qubits[qubit], qubits[n - qubit - 1])
        return circuit

    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit


machine.finalize()
