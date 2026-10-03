# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT

def simple_elitzur_vaidman():
    circuit = QCircuit()
    circuit << H(0) << CNOT(0, 1) << H(0)
    return circuit
