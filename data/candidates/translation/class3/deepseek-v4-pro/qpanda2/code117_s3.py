# EVAL_META: task_id=117, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, QOracle
import numpy as np

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    mat = np.asarray(unitary, dtype=complex)
    if mat.shape != (4, 4):
        mat = mat.reshape(4, 4)
    circ = QCircuit()
    circ << QOracle([q[0], q[1]], mat.tolist())
    return circ

machine.finalize()
