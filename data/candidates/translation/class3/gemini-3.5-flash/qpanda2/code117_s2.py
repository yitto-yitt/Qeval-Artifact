# EVAL_META: task_id=117, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

# Initialize CPUQVM globally
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    # Convert unitary to a 1D list of complex numbers (QStat)
    qstat = [complex(x) for x in np.array(unitary).flatten()]
    # Decompose the unitary matrix into a QCircuit
    circuit = matrix_decompose(q, qstat)
    return circuit

# Manual Cleanup
machine.finalize()
