# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT, S, Z

def create_cy_gate():
    circuit = QCircuit(2)
    circuit << Z(1)
    circuit << S(1)
    circuit << CNOT(0, 1)
    circuit << S(1)
    return circuit
