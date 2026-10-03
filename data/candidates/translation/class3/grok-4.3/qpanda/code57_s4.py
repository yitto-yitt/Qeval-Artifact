# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import *

def create_swap_gate():
    circuit = QCircuit()
    q = Qubit(2)
    circuit << CNOT(q[0], q[1]) << CNOT(q[1], q[0]) << CNOT(q[0], q[1])
    return circuit
