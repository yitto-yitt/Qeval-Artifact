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
    heads_count = result.get('0', 0)
    tails_count = result.get('1', 0)
    
    total = heads_count + tails_count
    
    prob_heads = heads_count / total if total > 0 else 0.0
    prob_tails = tails_count / total if total > 0 else 0.0
    
    machine.destroy()
    
    return {'Heads': prob_heads, 'Tails': prob_tails}
