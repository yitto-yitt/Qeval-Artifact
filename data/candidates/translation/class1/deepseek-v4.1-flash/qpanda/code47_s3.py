# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, Measure

def random_coin_flip(samples):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc()
    c = qvm.cAlloc()
    prog = QProg()
    prog << H(q) << Measure(q, c)
    result = qvm.run(prog, samples)
    counts = result.get_counts()
    total = sum(counts.values())
    return {'Heads': counts.get('0', 0) / total, 'Tails': counts.get('1', 0) / total}
