# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import init_qvm, finalize, qAlloc_many, QProg, H, CNOT, prob_run_dict

def calculate_stabilizer_state_info():
    init_qvm()
    q = qAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    result = prob_run_dict(prog, q, -1)
    finalize()
    return result
