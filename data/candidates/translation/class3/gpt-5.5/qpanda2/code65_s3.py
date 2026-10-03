# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
from math import pi
import atexit

_MAX_QUBITS = 64
machine = CPUQVM()
machine.set_configure(_MAX_QUBITS, _MAX_QUBITS)
machine.init_qvm()
qubits = machine.qAlloc_many(_MAX_QUBITS)
atexit.register(lambda: machine.finalize())

def QFT(n):
    circuit = QCircuit()

    def swap_registers(circuit, n):
        for qubit in range(n // 2):
            circuit.insert(SWAP(qubits[qubit], qubits[n - qubit - 1]))
        return circuit

    def qft_rotations(circuit, n):
        if n == 0:
            return circuit
        n -= 1
        circuit.insert(H(qubits[n]))
        for qubit in range(n):
            circuit.insert(CR(qubits[qubit], qubits[n], pi / (2 ** (n - qubit))))
        qft_rotations(circuit, n)
        return circuit

    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
