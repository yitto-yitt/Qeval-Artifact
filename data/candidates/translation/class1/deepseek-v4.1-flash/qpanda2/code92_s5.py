# EVAL_META: task_id=92, framework=qpanda2, class=1
from pyqpanda import CPUQVM, QProg, H, CNOT

def calculate_stabilizer_state_info():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    probabilities = machine.prob_run_dict(prog, q, -1)
    machine.finalize()
    return {k: v for k, v in probabilities.items() if abs(v) > 1e-12}
