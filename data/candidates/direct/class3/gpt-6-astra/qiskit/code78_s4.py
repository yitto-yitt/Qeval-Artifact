# EVAL_META: task_id=78, framework=qiskit, class=3
from math import pi
from qiskit import QuantumCircuit


def qft_no_swaps(num_qubits):
    circuit = QuantumCircuit(num_qubits, name="IQFT")
    for target in range(num_qubits):
        for control in range(target):
            circuit.cp(-pi / (2 ** (target - control)), control, target)
        circuit.h(target)
    return circuit
