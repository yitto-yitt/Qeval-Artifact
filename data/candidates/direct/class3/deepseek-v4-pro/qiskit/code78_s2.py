# EVAL_META: task_id=78, framework=qiskit, class=3
import math
from qiskit import QuantumCircuit

def qft_no_swaps(num_qubits):
    qc = QuantumCircuit(num_qubits)
    for i in range(num_qubits - 1, -1, -1):
        qc.h(i)
        for j in range(i - 1, -1, -1):
            qc.cp(-math.pi / (2 ** (i - j)), j, i)
    return qc
