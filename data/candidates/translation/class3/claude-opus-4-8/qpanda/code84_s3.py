# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, U3, QGate

def controlled_custom_unitary_circuit():
    qc = QCircuit(2)
    gate = U3(1, 0.3, 0.2, 0.1)
    gate.control([0])
    qc << gate
    return qc
