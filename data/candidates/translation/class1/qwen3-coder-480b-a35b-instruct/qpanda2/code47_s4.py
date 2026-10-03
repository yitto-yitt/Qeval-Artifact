# EVAL_META: task_id=47, framework=qpanda2, class=1
import pyqpanda as pq
import math

def random_coin_flip(samples):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(1)
    cbits = machine.cAlloc_many(1)
    
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.Measure(qubits[0], cbits[0]))
    
    result = machine.run_with_configuration(prog, cbits, samples)
    
    # Count the results
    heads_count = 0
    tails_count = 0
    
    for key, value in result.items():
        if key == '0':
            heads_count = value
        elif key == '1':
            tails_count = value
    
    total = samples
    return {'Heads': heads_count / total, 'Tails': tails_count / total}
