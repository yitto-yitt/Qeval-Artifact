# EVAL_META: task_id=47, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def random_coin_flip(samples):
    init(QMachineType.CPU)
    q = qAlloc_many(1)
    c = cAlloc_many(1)
    prog = QProg()
    prog << H(q[0]) << Measure(q[0], c[0])
    counts = run_with_configuration(prog, c, samples)
    total = builtins.sum(counts.values())
    heads = counts.get('0', 0) / total
    tails = counts.get('1', 0) / total
    finalize()
    return {'Heads': heads, 'Tails': tails}
