# EVAL_META: task_id=47, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def random_coin_flip(samples):
    qvm = init_quantum_machine(QMachineType.CPU)
    q = qvm.qAlloc(1)
    c = qvm.cAlloc(1)
    
    prog = QProg()
    prog << H(q[0])
    prog << Measure(q[0], c[0])
    
    counts = run_with_configuration(prog, c, samples)
    
    total = builtins.sum(counts.values())
    
    heads = counts.get('0', 0) / total
    tails = counts.get('1', 0) / total
    
    return {'Heads': heads, 'Tails': tails}
