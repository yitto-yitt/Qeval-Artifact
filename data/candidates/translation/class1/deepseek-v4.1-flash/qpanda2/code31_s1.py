# EVAL_META: task_id=31, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def sampler_qiskit():
    machine = CPUQVM()
    machine.init_qvm()
    try:
        machine.set_random_seed(42)
    except Exception:
        pass
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << measure_all(q, c)
    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
