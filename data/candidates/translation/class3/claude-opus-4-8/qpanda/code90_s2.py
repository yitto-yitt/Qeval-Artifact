# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, X, H

def create_custom_controlled():
    qubits = list(range(4))

    x_gate = X(1)
    x_gate.set_control([0, 3])

    h_gate = H(2)
    h_gate.set_control([0, 3])

    circuit = QCircuit()
    circuit << x_gate
    circuit << h_gate

    prog = QProg()
    prog << circuit
    return prog
