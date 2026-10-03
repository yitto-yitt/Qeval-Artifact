# EVAL_META: task_id=145, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, H, CR, SWAP

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(32)


def qft_inverse(n):
    circ = QCircuit()

    # Inverse QFT: reverse of the forward QFT

    # First, undo the swaps from the forward QFT
    for i in range(n // 2):
        circ << SWAP(qubits[i], qubits[n - 1 - i])

    # Then apply the inverse of the rotation/H gates in reverse order
    for j in reversed(range(n)):
        for k in reversed(range(j)):
            angle = -np.pi / (2 ** (j - k))
            circ << CR(qubits[k], qubits[j], angle)
        circ << H(qubits[j])

    return circ


if __name__ == "__main__":
    c = qft_inverse(3)
    print(c)
    machine.finalize()
