# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT


def apply_op_back():
    qubits = [0, 1, 2]
    circ = QCircuit(3)
    circ << H(qubits[0])
    circ << CNOT(qubits[0], qubits[1])
    circ << H(qubits[0])
    return circ
