# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def mcy(qc):
    qc.sdg(4)
    qc.mcx([0, 1, 2, 3], 4)
    qc.s(4)
    return qc
