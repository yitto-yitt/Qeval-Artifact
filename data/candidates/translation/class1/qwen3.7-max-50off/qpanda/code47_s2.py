# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import QMachine, QProg, H, Measure

def random_coin_flip(samples):
    qm = QMachine()
    q = qm.qAlloc(1)
    c = qm.cAlloc(1)
    prog = QProg()
    prog << H(q[0])
    prog << Measure(q[0], c[0])
    counts = qm.run(prog, samples)
    
    str_counts = {str(k): v for k, v in counts.items()}
    total = sum(str_counts.values())
    
    heads = str_counts.get('0', 0)
    tails = str_counts.get('1', 0)
    
    return {'Heads': heads / total, 'Tails': tails / total}
