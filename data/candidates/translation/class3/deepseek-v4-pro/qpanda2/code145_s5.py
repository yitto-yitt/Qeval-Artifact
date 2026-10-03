# EVAL_META: task_id=145, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_qubit_blocks = []

try:
    _CP = CP
except NameError:
    _CP = None

try:
    _SWAP = SWAP
except NameError:
    _SWAP = None

def _get_qubits(n):
    if n <= 0:
        return []
    for block in _qubit_blocks:
        if len(block) >= n:
            return block[:n]
    block = machine.qAlloc_many(n)
    _qubit_blocks.append(block)
    return block[:n]

def qft_inverse(n):
    if n <= 0:
        return QCircuit()

    q = _get_qubits(n)
    circ = QCircuit()

    # Inverse swaps (Qiskit QFT has do_swaps=True by default)
    if _SWAP is not None:
        for i in range(n // 2):
            circ << _SWAP(q[i], q[n - 1 - i])
    else:
        for i in range(n // 2):
            circ << CNOT(q[i], q[n - 1 - i])
            circ << CNOT(q[n - 1 - i], q[i])
            circ << CNOT(q[i], q[n - 1 - i])

    # Inverse QFT rotations
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            angle = -np.pi / (2 ** (j - i))
            if _CP is not None:
                circ << _CP(q[j], q[i], angle)
            else:
                half = angle / 2.0
                circ << RZ(q[j], half)
                circ << RZ(q[i], half)
                circ << CNOT(q[j], q[i])
                circ << RZ(q[i], -half)
                circ << CNOT(q[j], q[i])
        circ << H(q[i])

    return circ

machine.finalize()
