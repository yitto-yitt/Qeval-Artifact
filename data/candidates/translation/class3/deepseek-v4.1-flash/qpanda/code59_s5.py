# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT, Qubit

def create_cz_gate():
    circuit = QCircuit()
    q0 = Qubit(0)
    q1 = Qubit(1)
    circuit << H(q1)
    circuit << CNOT(q0, q1)
    circuit << H(q1)
    return circuit
