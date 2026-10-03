# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import *

def init_random_3qubit(desired_vector):
    init(QMachineType.CPU)
    q = qAlloc_many(3)
    prog = QProg()
    state = [complex(amp) for amp in desired_vector]
    norm = sum(abs(x) ** 2 for x in state) ** 0.5
    if norm != 0:
        state = [x / norm for x in state]
    prog << init_qubit_state(q, state)
    probs = get_probabilities(prog, q)
    finalize()
    total = sum(abs(p) for p in probs)
    if total == 0:
        total = 1.0
    return {format(i, '03b'): abs(p) / total for i, p in enumerate(probs)}
