# EVAL_META: task_id=145, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, H, CR, SWAP
import math

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(64)


def qft_inverse(n):
    circuit = QCircuit()

    for i in range(n // 2):
        circuit << SWAP(qubits[i], qubits[n - 1 - i])

    for j in range(n):
        for k in range(j):
            angle = -math.pi / (2 ** (j - k))
            circuit << CR(qubits[k], qubits[j], angle)
        circuit << H(qubits[j])

    return circuit


if __name__ == "__main__":
    qft_inverse(3)

machine.finalize()
