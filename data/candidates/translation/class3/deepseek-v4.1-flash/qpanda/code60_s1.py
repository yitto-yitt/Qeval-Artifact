# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT, S, SDG

def create_cy_gate():
    circuit = QCircuit()
    circuit << SDG(1)
    circuit << CNOT(0, 1)
    circuit << S(1)
    return circuit
