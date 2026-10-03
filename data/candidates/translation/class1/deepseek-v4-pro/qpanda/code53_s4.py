# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X

def xor_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(8)

    prog = QProg()
    for i in range(8):
        if (a >> i) & 1:
            prog << X(q[i])
        if (b >> i) & 1:
            prog << X(q[i])

    result = machine.prob_run_dict(prog, q)
    return {key: prob for key, prob in result.items() if prob > 0}
