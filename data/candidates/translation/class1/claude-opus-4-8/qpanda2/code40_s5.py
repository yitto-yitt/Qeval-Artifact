# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
import numpy as np
from pyqpanda import CPUQVM, amplitude_encode

def init_random_3qubit(desired_vector):
    vec = np.asarray(desired_vector, dtype=complex)
    norm = np.linalg.norm(vec)
    if norm != 0:
        vec = vec / norm

    qvm = CPUQVM()
    qvm.init_qvm()
    qvm.set_configure(50, 50)
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)

    prog = amplitude_encode(qubits, vec.tolist())
    from pyqpanda import measure_all
    prog << measure_all(qubits, cbits)

    shots = 8192
    counts = qvm.run_with_configuration(prog, cbits, shots)
    qvm.finalize()

    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
