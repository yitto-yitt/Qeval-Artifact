# EVAL_META: task_id=31, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QProg, H, CNOT, Measure
import pyqpanda3 as pq

def sampler_qiskit():
    try:
        pq.set_seed(42)
    except Exception:
        pass
        
    qvm = QuantumMachine()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    prog << Measure(q[0], c[0]) << Measure(q[1], c[1])
    
    try:
        probs = qvm.prob_run_tuple_list(prog, q, -1)
    except Exception:
        probs = qvm.get_prob_tuple_list(prog, q, -1)
        
    res = {}
    for state, prob in probs:
        if isinstance(state, int):
            bs = format(state, '02b')
        else:
            bs = str(state).zfill(2)
        if prob > 1e-8:
            res[bs] = prob
            
    if not res:
        try:
            counts = qvm.run(prog, 1024)
        except Exception:
            counts = qvm.run(prog, c, 1024)
        total = sum(counts.values())
        res = {str(k).zfill(2): v / total for k, v in counts.items()}
        
    return res
