# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import init, qAlloc_many, create_empty_qprog, H, CNOT, prob_run_dict, finalize

def calculate_stabilizer_state_info():
    init()
    q = qAlloc_many(2)
    prog = create_empty_qprog()
    prog.insert(H(q[0])).insert(CNOT(q[0], q[1]))
    probabilities_dict = prob_run_dict(prog, q)
    finalize()
    return probabilities_dict
