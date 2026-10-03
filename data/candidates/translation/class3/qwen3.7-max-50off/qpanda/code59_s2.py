# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, H, CNOT

def create_cz_gate():
    q0 = Qubit()
    q1 = Qubit()
    circuit = QCircuit()
    circuit << H(q1)
    circuit << CNOT(q0, q1)
    circuit << H(q1)
    return circuit
