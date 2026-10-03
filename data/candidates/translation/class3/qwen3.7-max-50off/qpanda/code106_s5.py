# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT, T, X

def compose_cnot_dihedral():
    circ = QCircuit()
    q = circ.allocate_qubits(2)
    circ << CNOT(q[0], q[1])
    circ << T(q[0])
    circ << CNOT(q[0], q[1])
    circ << T(q[0])
    circ << X(q[1])
    return circ
