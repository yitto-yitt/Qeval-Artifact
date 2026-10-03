# EVAL_META: task_id=47, framework=qpanda2, class=1
import builtins
from pyqpanda import QProg, H, Measure, CPUQVM

def random_coin_flip(samples):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(1)
    prog = QProg()
    prog << H(q[0])
    prog << Measure(q[0], c[0])
    counts = qvm.run_with_configuration(prog, c, samples)
    qvm.finalize()
    total = builtins.sum(counts.values())
    if total == 0:
        return {'Heads': 0.5, 'Tails': 0.5}
    heads = counts.get('0', counts.get(0, 0))
    tails = counts.get('1', counts.get(1, 0))
    return {'Heads': heads / total, 'Tails': tails / total}
