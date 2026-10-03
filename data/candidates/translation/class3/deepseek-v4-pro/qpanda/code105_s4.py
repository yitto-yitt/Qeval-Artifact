# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit


def initialize_cnot_dihedral():
    qc = QuantumCircuit(2)
    qc.cnot(0, 1)
    qc.t(0)
    return qc
