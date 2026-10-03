# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT, QubitAllocator

def simple_elitzur_vaidman():
    q = QubitAllocator(2)
    circuit = QCircuit()
    circuit << H(q[0]) << CNOT(q[0], q[1]) << H(q[0])
    return circuit
