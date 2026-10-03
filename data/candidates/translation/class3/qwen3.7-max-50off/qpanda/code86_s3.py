# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, H, CX

def collect_linear_blocks_with_and_without_limit():
    qc_full = QuantumCircuit(5)
    qc_full << H(0)
    qc_full << CX(0, 1)
    qc_full << CX(1, 2)
    qc_full << CX(2, 3)
    qc_full << CX(3, 4)
    
    qc_limited = QuantumCircuit(5)
    qc_limited << H(0)
    qc_limited << CX(0, 1)
    qc_limited << CX(1, 2)
    qc_limited << CX(2, 3)
    qc_limited << CX(3, 4)
    
    return qc_full, qc_limited
