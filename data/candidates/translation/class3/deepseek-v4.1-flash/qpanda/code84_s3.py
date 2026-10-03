# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, U3

def controlled_custom_unitary_circuit():
    qc = QCircuit(2)
    custom_gate = U3(1, 0.3, 0.2, 0.1).control(0)
    qc << custom_gate
    return qc
