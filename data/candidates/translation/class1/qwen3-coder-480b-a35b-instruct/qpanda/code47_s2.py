# EVAL_META: task_id=47, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *
import math

def random_coin_flip(samples):
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)
    
    prog = QProg()
    prog << H(q[0]) << Measure(q[0], c[0])
    
    result = run_with_configuration(prog, c, samples)
    
    heads_count = result.get("0", 0)
    tails_count = result.get("1", 0)
    total = heads_count + tails_count
    
    prob_heads = heads_count / total if total > 0 else 0.5
    prob_tails = tails_count / total if total > 0 else 0.5
    
    destroy_quantum_machine(machine)
    
    return {'Heads': prob_heads, 'Tails': prob_tails}
