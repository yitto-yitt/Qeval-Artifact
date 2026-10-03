# EVAL_META: task_id=41, framework=qpanda2, class=3
import numpy as np
import pyqpanda

machine = pyqpanda.CPUQVM()
machine.init()
q = machine.qAlloc_many(3)

def compose_op():
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    I = np.eye(2, dtype=complex)
    
    # Y on qubit 2, I on qubit 1, X on qubit 0
    return np.kron(Y, np.kron(I, X))

machine.finalize()
