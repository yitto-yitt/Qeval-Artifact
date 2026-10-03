# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import QProg, H, measure, CPUQVM

def random_coin_flip(samples):
    prog = QProg()
    prog << H(0)
    prog << measure(0, 0)
    qvm = CPUQVM()
    qvm.run(prog, samples)
    counts = qvm.result().get_counts()
    total = sum(counts.values())
    return {'Heads': counts.get('0', 0) / total, 'Tails': counts.get('1', 0) / total}
