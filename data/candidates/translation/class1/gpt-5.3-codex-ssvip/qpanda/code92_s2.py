# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import *

def calculate_stabilizer_state_info():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])

    state = machine.prob_run_dict(prog, q)
    machine.finalize()

    return state
