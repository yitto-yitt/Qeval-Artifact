# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import QMachine, QCircuit, S, Sdag, CNOT

def create_cy_gate():
    qm = QMachine()
    q = qm.qAlloc(2)
    circ = QCircuit()
    circ << Sdag(q[1]) << CNOT(q[0], q[1]) << S(q[1])
    return circ
