# EVAL_META: task_id=1, framework=qpanda2, class=1
from pyqpanda import *

def run_bell_state_simulator():
    init(QMachineType.CPU)
    q = qAlloc_many(2)
    c = cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << MeasureAll(q, c)
    shots = 1000
    counts = run_with_configuration(prog, c, shots)
    return {key: value / shots for key, value in counts.items()}
