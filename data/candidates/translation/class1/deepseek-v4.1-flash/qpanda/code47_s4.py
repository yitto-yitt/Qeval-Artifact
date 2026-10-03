# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import QProg, CPUQVM, H, measure

def random_coin_flip(samples):
    prog = QProg()
    prog << H(0)
    prog << measure(0, 0)

    machine = CPUQVM()
    machine.run(prog, samples)
    result = machine.result()
    counts = result.get_counts()

    heads = 0
    tails = 0
    for key, value in counts.items():
        if '1' in str(key):
            tails += value
        else:
            heads += value

    total = heads + tails
    return {'Heads': heads / total, 'Tails': tails / total}
