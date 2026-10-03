# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, Measure

def random_coin_flip(samples):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)
    prog = QProg()
    prog << H(q[0]) << Measure(q[0], c[0])
    result = machine.run_with_shots(prog, samples)
    counts = result.get_counts() if hasattr(result, 'get_counts') else result
    counts = {str(k): v for k, v in counts.items()}
    total = sum(counts.values())
    heads = counts.get('0', 0)
    tails = counts.get('1', 0)
    return {'Heads': heads / total, 'Tails': tails / total}
