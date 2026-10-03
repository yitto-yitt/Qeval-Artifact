# EVAL_META: task_id=1, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def run_bell_state_simulator():
    init(QMachineType.CPU)
    q = qAlloc_many(2)
    c = cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << MeasureAll(q, c)
    counts = run_with_configuration(prog, c, 1000)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
