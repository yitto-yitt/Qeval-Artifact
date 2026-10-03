# EVAL_META: task_id=78, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)

def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    for i in reversed(range(num_qubits)):
        for j in reversed(range(i + 1, num_qubits)):
            angle = -np.pi / (2 ** (j - i))
            circuit << CR(qubits[j], qubits[i], angle)
        circuit << H(qubits[i])
    return circuit

if __name__ == "__main__":
    machine.finalize()
