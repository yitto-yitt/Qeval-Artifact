# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import *

def random_coin_flip(samples):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(1)
    prog = QProg()
    prog << H(q[0]) << Measure(q[0], c[0])
    result = qvm.run_with_configuration(prog, c, samples)
    total = sum(result.values())
    return {'Heads': result.get(0, 0) / total, 'Tails': result.get(1, 0) / total}
