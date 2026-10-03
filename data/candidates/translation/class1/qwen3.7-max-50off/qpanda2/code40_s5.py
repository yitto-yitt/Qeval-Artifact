# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def init_random_3qubit(desired_vector):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)
    
    if hasattr(desired_vector, 'tolist'):
        vec = desired_vector.tolist()
    else:
        vec = list(desired_vector)
        
    qvm.init_state(q, vec)
    
    prog = pq.QProg()
    for i in range(3):
        prog += pq.Measure(q[i], c[i])
    
    counts = qvm.run_with_configuration(prog, c, 1000)
    
    total = builtins.sum(counts.values())
    
    probs = {}
    for k, v in counts.items():
        if isinstance(k, int):
            k_str = format(k, '03b')
        else:
            k_str = str(k).replace(' ', '')
            if len(k_str) < 3:
                k_str = k_str.zfill(3)
        probs[k_str] = v / total
        
    return probs
