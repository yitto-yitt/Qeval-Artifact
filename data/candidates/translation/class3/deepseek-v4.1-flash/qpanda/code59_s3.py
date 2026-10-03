# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT, qAlloc

def create_cz_gate():
    q = qAlloc(2)
    circuit = QCircuit()
    circuit << H(q[1])
    circuit << CNOT(q[0], q[1])
    circuit << H(q[1])
    return circuit
