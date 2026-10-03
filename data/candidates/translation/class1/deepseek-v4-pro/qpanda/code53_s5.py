# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import QMachineFactory, QProg, X


def xor_gate(a, b):
    qvm = QMachineFactory.create_qvm()
    q = qvm.qAlloc_many(8)

    prog = QProg()
    for i in range(8):
        if ((a ^ b) >> i) & 1:
            prog << X(q[i])

    result = qvm.prob_run_dict(prog, q)
    return {key: float(prob) for key, prob in result.items() if prob > 0}
