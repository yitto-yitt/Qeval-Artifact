# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import *

def calculate_stabilizer_state_info():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])

    state = machine.get_qstate(prog)
    machine.finalize()

    probs = {}
    n = 2
    for i, amp in enumerate(state):
        p = (amp.real * amp.real + amp.imag * amp.imag)
        if p > 1e-15:
            key = format(i, f"0{n}b")
            probs[key] = p
    return probs
