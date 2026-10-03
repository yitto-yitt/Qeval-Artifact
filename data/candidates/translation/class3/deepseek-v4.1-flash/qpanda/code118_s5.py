# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QGate

def create_c3sx_circuit():
    circuit = QCircuit()
    circuit << QGate("C3SX", [0, 1, 2, 3])
    return circuit
