# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QVec, CU3

def controlled_custom_unitary_circuit():
    q = QVec(2)
    circuit = QCircuit()
    circuit << CU3(q[0], q[1], 0.3, 0.2, 0.1)
    return circuit
