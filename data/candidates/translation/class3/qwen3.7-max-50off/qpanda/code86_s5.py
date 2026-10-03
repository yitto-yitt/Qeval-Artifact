# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def collect_linear_blocks_with_and_without_limit():
    qc = QuantumCircuit(5)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.cx(2, 3)
    qc.cx(3, 4)
    
    return qc, qc
