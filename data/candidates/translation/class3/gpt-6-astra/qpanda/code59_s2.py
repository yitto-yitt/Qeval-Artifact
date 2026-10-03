# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import QProg, H, CNOT

def create_cz_gate():
    circuit = QProg()
    circuit << H(1) << CNOT(0, 1) << H(1)
    return circuit
