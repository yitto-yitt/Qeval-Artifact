# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import QuantumMachine, QCircuit

def create_unitary_from_matrix():
    qm = QuantumMachine()
    q = qm.qAlloc(2)
    cir = QCircuit()
    cir.x(q[1])
    cir.cx(q[1], q[0])
    return cir
