# EVAL_META: task_id=78, framework=qiskit, class=3
from math import pi
from qiskit import QuantumCircuit


def qft_no_swaps(num_qubits):
    circuit = QuantumCircuit(num_qubits, name="IQFT_no_swaps")
    for j in range(num_qubits):
        for k in range(j):
            circuit.cp(-pi / (2 ** (j - k)), j, k)
        circuit.h(j)
    return circuit
