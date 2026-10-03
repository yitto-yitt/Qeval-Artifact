# EVAL_META: task_id=78, framework=qiskit, class=3
import math
from qiskit import QuantumCircuit


def qft_no_swaps(num_qubits):
    circuit = QuantumCircuit(num_qubits, name="IQFT_no_swaps")
    for j in range(num_qubits):
        for m in range(j):
            circuit.cp(-math.pi / (2 ** (j - m)), m, j)
        circuit.h(j)
    return circuit
