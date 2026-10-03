# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT

def simple_elitzur_vaidman():
    circuit = QCircuit(2)
    circuit << H(0)
    circuit << CNOT(0, 1)
    circuit << H(0)
    return circuit
