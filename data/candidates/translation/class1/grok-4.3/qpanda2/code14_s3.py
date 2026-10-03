# EVAL_META: task_id=14, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def bell_each_shot():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << measure_all(q, c)
    counts = machine.run_with_configuration(prog, c, 10)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
