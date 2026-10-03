# EVAL_META: task_id=92, framework=qpanda2, class=1
from pyqpanda import *

def calculate_stabilizer_state_info():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])

    state = machine.get_qstate(prog)
    machine.finalize()

    probs = {
        "00": float(abs(state[0]) ** 2),
        "01": float(abs(state[1]) ** 2),
        "10": float(abs(state[2]) ** 2),
        "11": float(abs(state[3]) ** 2),
    }
    return probs
