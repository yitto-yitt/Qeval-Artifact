# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def mcy(qc):
    qc.mcy([0, 1, 2, 3], 4)
    return qc
