# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, U3, Qubit

def controlled_custom_unitary_circuit():
    q0 = Qubit()
    q1 = Qubit()
    qc = QCircuit()
    qc << U3(q1, 0.3, 0.2, 0.1).control([q0])
    return qc
