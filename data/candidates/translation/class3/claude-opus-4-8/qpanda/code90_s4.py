# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, X, H

def create_custom_controlled():
    qubits = list(range(4))

    x_gate = X(1)
    x_gate.control([0, 3])

    h_gate = H(2)
    h_gate.control([0, 3])

    circ = QCircuit()
    circ << x_gate
    circ << h_gate

    prog = QProg()
    prog << circ
    return prog
