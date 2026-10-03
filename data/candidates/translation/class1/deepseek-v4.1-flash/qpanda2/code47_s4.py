# EVAL_META: task_id=47, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def random_coin_flip(samples):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(1)
    prog = QProg()
    prog << H(q[0]) << measure(q[0], c[0])
    result = qvm.run_with_configuration(prog, c, samples)
    total = builtins.sum(result.values())
    heads = result.get(0, 0)
    tails = result.get(1, 0)
    qvm.finalize()
    return {'Heads': heads / total, 'Tails': tails / total}
