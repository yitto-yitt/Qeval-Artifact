# EVAL_META: task_id=14, framework=qpanda, class=1
from pyqpanda3.core import *

def bell_each_shot():
    init_qvm()
    q = qalloc(2)
    c = cbit_alloc(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << measure_all(q, c)

    counts = run_with_configuration(prog, c, 10)
    finalize_qvm()

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
