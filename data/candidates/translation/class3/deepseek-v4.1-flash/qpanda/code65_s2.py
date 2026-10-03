# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CP, SWAP, qAlloc_many
from numpy import pi

def QFT(n):
    circuit = QCircuit()
    if n == 0:
        return circuit
    qubits = qAlloc_many(n)

    def swap_registers():
        for qubit in range(n // 2):
            circuit << SWAP(qubits[qubit], qubits[n - qubit - 1])

    def qft_rotations(k):
        if k == 0:
            return
        k -= 1
        circuit << H(qubits[k])
        for qubit in range(k):
            circuit << CP(qubits[qubit], qubits[k], pi / 2 ** (k - qubit))
        qft_rotations(k)

    qft_rotations(n)
    swap_registers()
    return circuit
