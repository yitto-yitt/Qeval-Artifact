# EVAL_META: task_id=84, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
import numpy as np


def controlled_custom_unitary_circuit():
    theta, phi, lam = 0.3, 0.2, 0.1
    custom = QuantumCircuit(1, name="custom_u")
    custom.u(theta, phi, lam, 0)
    gate = custom.to_gate()

    qc = QuantumCircuit(2)
    controlled_gate = gate.control(1)
    qc.append(controlled_gate, [0, 1])
    return qc
