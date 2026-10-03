# EVAL_META: task_id=78, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, Qubit, H, CR
import numpy as np

machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(10)

def qft_no_swaps(num_qubits):
    circuit = QCircuit()
    qubits = [Qubit(i) for i in range(num_qubits)]
    for i in reversed(range(num_qubits)):
        for j in reversed(range(i + 1, num_qubits)):
            circuit << CR(qubits[j], qubits[i], -np.pi / 2**(j - i))
        circuit << H(qubits[i])
    return circuit

machine.finalize()
