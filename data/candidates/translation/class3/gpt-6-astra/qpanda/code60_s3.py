# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import QProg, S, CNOT

def create_cy_gate():
    circuit = QProg()
    circuit << S(1).dagger() << CNOT(0, 1) << S(1)
    return circuit
