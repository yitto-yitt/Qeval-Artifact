# EVAL_META: task_id=78, framework=qiskit, class=3
from math import pi
from qiskit import QuantumCircuit


def qft_no_swaps(num_qubits):
    circuit = QuantumCircuit(num_qubits)
    for j in range(num_qubits):
        for m in range(j):
            circuit.cp(-pi / (2 ** (j - m)), j, m)
        circuit.h(j)
    return circuit
