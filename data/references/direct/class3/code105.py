# EVAL_META: task_id=105, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.quantum_info import CNOTDihedral


def initialize_cnot_dihedral():
    circ = QuantumCircuit(2)
    circ.cx(0, 1)
    circ.t(0)
    elem = CNOTDihedral(circ)
    return elem


# ==================================================
