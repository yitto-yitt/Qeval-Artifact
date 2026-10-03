# EVAL_META: task_id=92, framework=qpanda2, class=1
from pyqpanda import *

def calculate_stabilizer_state_info():
    init(QMachineType.CPU)
    q = qAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    probabilities = prob_run_dict(prog, q)
    finalize()
    return {state: prob for state, prob in probabilities.items() if prob != 0}
