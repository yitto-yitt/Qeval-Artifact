# EVAL_META: task_id=78, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def qft_no_swaps(num_qubits):
    circuit = QuantumCircuit(num_qubits, name="IQFT_no_swaps")
    for i in reversed(range(num_qubits)):
        for j in reversed(range(i + 1, num_qubits)):
            circuit.cp(-np.pi / (2 ** (j - i)), j, i)
        circuit.h(i)
    return circuit
