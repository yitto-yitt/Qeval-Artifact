# EVAL_META: task_id=2, framework=qiskit, class=2
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def create_bell_statevector():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return Statevector(qc)
