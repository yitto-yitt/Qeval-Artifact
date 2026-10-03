# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
from math import pi

machine = CPUQVM()
machine.init()
_qubit_cache = []

def QFT(n):
    global _qubit_cache

    qubits = machine.qAlloc_many(n)
    _qubit_cache.extend(qubits)

    def swap_registers(circuit, n, qubits):
        for qubit in range(n // 2):
            circuit << SWAP(qubits[qubit], qubits[n - qubit - 1])
        return circuit

    def qft_rotations(circuit, n, qubits):
        if n == 0:
            return circuit
        n -= 1
        circuit << H(qubits[n])
        for qubit in range(n):
            circuit << CP(qubits[qubit], qubits[n], pi / 2 ** (n - qubit))
        qft_rotations(circuit, n, qubits)

    circuit = QCircuit()
    qft_rotations(circuit, n, qubits)
    swap_registers(circuit, n, qubits)

    prog = QProg()
    prog << circuit
    return prog

machine.finalize()
