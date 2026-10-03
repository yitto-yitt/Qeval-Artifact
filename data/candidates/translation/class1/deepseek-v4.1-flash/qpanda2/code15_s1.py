# EVAL_META: task_id=15, framework=qpanda2, class=1
from pyqpanda import *

def noisy_bell():
    shots = 1000
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << measure_all(q, c)
    counts = machine.run_with_configuration(prog, c, shots)
    machine.finalize()
    return {key: value / shots for key, value in counts.items()}
