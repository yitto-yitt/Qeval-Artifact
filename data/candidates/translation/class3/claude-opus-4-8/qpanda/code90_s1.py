# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, X, H

def create_custom_controlled():
    qubits = list(range(4))
    controls = [qubits[0], qubits[3]]

    sub = QCircuit()
    sub << X(qubits[1])
    sub << H(qubits[2])

    controlled = sub.control(controls)

    circuit = QCircuit()
    circuit << controlled

    prog = QProg()
    prog << circuit
    return prog
