# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_operator():
    qc = QuantumCircuit(2)
    qc.cnot(0, 1)
    qc.cnot(1, 0)
    qc.cnot(0, 1)
    return qc
