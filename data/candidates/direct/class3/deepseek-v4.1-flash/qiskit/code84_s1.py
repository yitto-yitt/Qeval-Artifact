# EVAL_META: task_id=84, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit.circuit.library import UGate


def controlled_custom_unitary_circuit():
    angles = [0.3, 0.2, 0.1]
    custom_gate = UGate(*angles)

    qc = QuantumCircuit(2)
    controlled_gate = custom_gate.control(1)
    qc.append(controlled_gate, [0, 1])

    return qc
