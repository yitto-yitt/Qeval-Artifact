# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT

def simple_elitzur_vaidman():
    q = [0, 1]
    circuit = QCircuit()
    circuit << H(q[0])
    circuit << CNOT(q[0], q[1])
    circuit << H(q[0])
    return circuit
