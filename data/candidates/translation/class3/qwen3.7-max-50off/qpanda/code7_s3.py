# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QMachine, Parameter

def create_parametrized_gate():
    theta = Parameter("theta")
    qm = QMachine()
    q = qm.allocate_qubits(1)
    circ = QCircuit()
    circ.rx(q[0], theta)
    return circ
