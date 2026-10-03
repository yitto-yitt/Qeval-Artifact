# EVAL_META: task_id=47, framework=qpanda, class=1
import pyqpanda3 as pq
from pyqpanda3.core import *

def random_coin_flip(samples):
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(1)
    cbits = machine.cAlloc_many(1)
    
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.Measure(qubits[0], cbits[0]))
    
    result = machine.run(prog, shots=samples)
    
    heads_count = 0
    tails_count = 0
    
    for res in result:
        if res == '0':
            heads_count += 1
        elif res == '1':
            tails_count += 1
    
    total = heads_count + tails_count
    return {
        'Heads': heads_count / total if total > 0 else 0.0,
        'Tails': tails_count / total if total > 0 else 0.0
    }
