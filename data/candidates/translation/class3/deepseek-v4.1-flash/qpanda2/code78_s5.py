# EVAL_META: task_id=78, framework=qpanda2, class=3
import math
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
all_qubits = machine.qAlloc_many(20)

def qft_no_swaps(num_qubits):
    qubits = all_qubits[:num_qubits]
    circuit = QCircuit()
    for j in reversed(range(num_qubits)):
        for k in reversed(range(j + 1, num_qubits)):
            angle = -math.pi / (2 ** (k - j))
            circuit << CR(qubits[k], qubits[j], angle)
        circuit << H(qubits[j])
    return circuit

if __name__ == "__main__":
    machine.finalize()
