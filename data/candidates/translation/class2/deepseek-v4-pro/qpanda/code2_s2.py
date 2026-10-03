# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import QuantumCircuit


def create_bell_statevector():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cnot(0, 1)
    return qc.statevector()
