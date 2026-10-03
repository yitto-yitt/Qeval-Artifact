# EVAL_META: task_id=78, framework=qiskit, class=3
import math
from qiskit import QuantumCircuit

def qft_no_swaps(num_qubits):
    qc = QuantumCircuit(num_qubits)
    for j in reversed(range(num_qubits)):
        for k in reversed(range(j + 1, num_qubits)):
            qc.cp(-math.pi / (2 ** (k - j)), k, j)
        qc.h(j)
    return qc
