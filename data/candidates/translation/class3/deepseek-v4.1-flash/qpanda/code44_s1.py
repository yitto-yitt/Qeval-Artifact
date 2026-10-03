# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CRY, X

def tensor_circuits():
    circuit = QCircuit()
    circuit << CRY(0, 1, 0.2)
    circuit << X(2)
    return circuit
