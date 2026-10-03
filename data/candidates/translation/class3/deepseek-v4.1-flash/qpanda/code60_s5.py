# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import *

def create_cy_gate():
    circuit = QCircuit()
    circuit << Sdg(1) << CNOT(0, 1) << S(1)
    return circuit
