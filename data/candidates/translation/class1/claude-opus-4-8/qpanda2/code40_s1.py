# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
import numpy as np
from pyqpanda import CPUQVM, amplitude_encode

def init_random_3qubit(desired_vector):
    vec = np.asarray(desired_vector, dtype=complex)
    vec = vec / np.linalg.norm(vec)

    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)

    prog = amplitude_encode(qubits, vec)
    for i in range(3):
        prog << pyqpanda_measure(qubits[i], cbits[i])

    shots = 4096
    result = qvm.run_with_configuration(prog, cbits, shots)
    qvm.finalize()

    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
