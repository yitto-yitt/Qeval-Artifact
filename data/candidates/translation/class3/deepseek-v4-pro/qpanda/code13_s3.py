# EVAL_META: task_id=13, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, U3, qAlloc_many, init_qvm

def custom_rotation_gate():
    init_qvm()
    qubits = qAlloc_many(1)
    circuit = QCircuit()
    circuit << U3(qubits[0], np.pi / 2, np.pi / 2, np.pi / 2)
    return circuit
