# EVAL_META: task_id=5, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QProg, X


def create_state_prep():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog << X(qubits[1])
    result = qvm.prob_run_dict(prog, qubits, -1)
    return result
