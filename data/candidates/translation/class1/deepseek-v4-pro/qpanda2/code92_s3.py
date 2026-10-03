# EVAL_META: task_id=92, framework=qpanda2, class=1
from pyqpanda import *

def calculate_stabilizer_state_info():
    init(QMachineType.CPU)
    q = qAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    probs = prob_run_dict(prog, q)
    finalize()
    return {k: float(v) for k, v in probs.items() if v > 1e-12}
