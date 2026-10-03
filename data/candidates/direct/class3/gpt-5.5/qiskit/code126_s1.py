# EVAL_META: task_id=126, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, process_fidelity
import numpy as np


def calculate_phase_difference_fidelity():
    circuit_1 = QuantumCircuit(1)
    circuit_1.h(0)

    circuit_2 = QuantumCircuit(1)
    circuit_2.global_phase = np.pi / 3
    circuit_2.h(0)

    operator_1 = Operator(circuit_1)
    operator_2 = Operator(circuit_2)

    return process_fidelity(operator_1, operator_2)
