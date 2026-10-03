# EVAL_META: task_id=47, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QProg, H, Measure

def random_coin_flip(samples):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)
    prog = QProg()
    prog << H(q[0]) << Measure(q[0], c[0])
    result = machine.run_with_configuration(prog, c, samples)
    machine.finalize()
    counts = {str(k): v for k, v in result.items()}
    total = builtins.sum(counts.values())
    return {
        'Heads': counts.get('0', 0) / total,
        'Tails': counts.get('1', 0) / total
    }
