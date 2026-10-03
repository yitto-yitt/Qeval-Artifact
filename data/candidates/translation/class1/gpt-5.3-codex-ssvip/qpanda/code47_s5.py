# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import *

def random_coin_flip(samples):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc()
    c = machine.cAlloc()
    prog = QProg()
    prog << H(q) << Measure(q, c)
    result = machine.run_with_configuration(prog, [c], int(samples))
    machine.finalize()
    total = sum(result.values()) if result else 0
    heads = result.get('0', 0) / total if total > 0 else 0.0
    tails = result.get('1', 0) / total if total > 0 else 0.0
    return {'Heads': heads, 'Tails': tails}
