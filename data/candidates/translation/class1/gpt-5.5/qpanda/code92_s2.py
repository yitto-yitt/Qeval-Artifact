# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import *

def calculate_stabilizer_state_info():
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    q = qvm.qAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])

    if hasattr(qvm, "prob_run_dict"):
        probs = qvm.prob_run_dict(prog, q, -1)
    elif hasattr(qvm, "prob_run"):
        probs = qvm.prob_run(prog, q, -1)
    else:
        probs = qvm.get_prob_dict(prog, q)

    if hasattr(qvm, "finalize"):
        qvm.finalize()

    return {k: v for k, v in dict(probs).items() if abs(v) > 1e-12}
