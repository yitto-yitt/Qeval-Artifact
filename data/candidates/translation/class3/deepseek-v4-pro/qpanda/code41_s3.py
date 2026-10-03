# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QCircuit, X, Y

def compose_op():
    qvm = CPUQVM()
    qvm.init()
    qubits = qvm.qAlloc_many(3)
    circ = QCircuit()
    circ << Y(qubits[0]) << X(qubits[2])
    return np.array(qvm.get_matrix(circ))
