# EVAL_META: task_id=40, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def init_random_3qubit(desired_vector):
    init(QMachineType.CPU)
    q = qAlloc_many(3)
    c = cAlloc_many(3)
    prog = QProg()
    prog << init_qubits(q, desired_vector)
    prog << measure_all(q, c)
    shots = 10000
    counts = run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    return {key[::-1]: value / total for key, value in counts.items()}
