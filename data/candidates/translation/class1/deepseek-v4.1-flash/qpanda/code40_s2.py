# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import *

def init_random_3qubit(desired_vector):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)
    prog = QProg()
    prog << amplitude_encode(q, desired_vector)
    prog << measure_all(q, c)
    result = machine.prob_run_dict(prog, c)
    machine.finalize()
    return result
