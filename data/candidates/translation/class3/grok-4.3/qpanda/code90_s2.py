# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def create_custom_controlled():
    qc1 = QCircuit(2)
    qc1.x(0)
    qc1.h(1)
    custom = qc1.to_gate().control(2)
    qc2 = QCircuit(4)
    qc2.append(custom, [0, 3, 1, 2])
    return qc2
