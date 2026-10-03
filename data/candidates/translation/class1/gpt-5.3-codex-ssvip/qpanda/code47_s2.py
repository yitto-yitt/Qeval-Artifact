# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import *

def random_coin_flip(samples):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc()
    c = qvm.cAlloc()

    prog = QProg()
    prog << H(q) << Measure(q, c)

    result = qvm.run_with_configuration(prog, [c], samples)
    qvm.finalize()

    total = sum(result.values()) if result else 0
    if total == 0:
        return {"Heads": 0.0, "Tails": 0.0}

    heads = result.get("0", 0) / total
    tails = result.get("1", 0) / total
    return {"Heads": heads, "Tails": tails}
