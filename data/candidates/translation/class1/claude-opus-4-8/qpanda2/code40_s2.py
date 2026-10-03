# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
import numpy as np
from pyqpanda import CPUQVM, amplitude_encode, measure_all

def init_random_3qubit(desired_vector):
    vec = np.asarray(desired_vector, dtype=complex)
    norm = np.linalg.norm(vec)
    if norm != 0:
        vec = vec / norm

    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)

    prog = qvm.create_empty_qprog() if hasattr(qvm, "create_empty_qprog") else None
    from pyqpanda import QProg
    prog = QProg()
    prog << amplitude_encode(qubits, vec)
    prog << measure_all(qubits, cbits)

    shots = 4096
    counts = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    qvm.finalize()
    return {key: value / total for key, value in counts.items()}
