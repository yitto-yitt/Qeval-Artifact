# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
import numpy as np
from pyqpanda import CPUQVM, amplitude_encode, QCircuit

def init_random_3qubit(desired_vector):
    vec = np.array(desired_vector, dtype=complex)
    vec = vec / np.linalg.norm(vec)

    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qubit_alloc(3)
    cbits = qvm.cbit_alloc(3)

    prog = qvm.qprog_init() if hasattr(qvm, "qprog_init") else None
    from pyqpanda import QProg, measure_all

    circuit = amplitude_encode(qubits, vec)

    prog = QProg()
    prog << circuit
    prog << measure_all(qubits, cbits)

    shots = 4096
    counts = qvm.run_with_configuration(prog, cbits, shots)
    qvm.finalize()

    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
