# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit


def compose_cnot_dihedral():
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    qc.t(0)
    qc.cx(0, 1)
    qc.t(0)
    qc.x(1)
    return qc
