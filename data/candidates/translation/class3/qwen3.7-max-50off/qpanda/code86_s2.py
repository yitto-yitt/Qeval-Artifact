# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def collect_linear_blocks_with_and_without_limit():
    qc1 = QuantumCircuit(5)
    qc1.h(0)
    qc1.cx(0, 1)
    qc1.cx(1, 2)
    qc1.cx(2, 3)
    qc1.cx(3, 4)

    qc2 = QuantumCircuit(5)
    qc2.h(0)
    qc2.cx(0, 1)
    qc2.cx(1, 2)
    qc2.cx(2, 3)
    qc2.cx(3, 4)

    return qc1, qc2
