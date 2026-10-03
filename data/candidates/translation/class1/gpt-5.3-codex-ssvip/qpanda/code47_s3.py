# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import *

def random_coin_flip(samples):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)

    prog = QProg()
    prog << H(q[0]) << Measure(q[0], c[0])

    result = machine.run_with_configuration(prog, c, samples)
    machine.finalize()

    total = sum(result.values()) if result else 0
    if total == 0:
        return {'Heads': 0.0, 'Tails': 0.0}

    heads = result.get('0', 0) / total
    tails = result.get('1', 0) / total
    return {'Heads': heads, 'Tails': tails}
