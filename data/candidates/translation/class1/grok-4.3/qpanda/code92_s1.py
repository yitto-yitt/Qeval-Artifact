# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT

def calculate_stabilizer_state_info():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    probabilities_dict = qvm.prob_run_dict(prog, q)
    qvm.finalize()
    return probabilities_dict
