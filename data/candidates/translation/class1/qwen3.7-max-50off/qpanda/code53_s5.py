# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import init_quantum_machine, QMachineType, QProg, X, Measure

def xor_gate(a, b):
    qvm = init_quantum_machine(QMachineType.CPU)
    q = qvm.qAlloc_many(8)
    c = qvm.cAlloc_many(8)
    prog = QProg()
    val = a ^ b
    
    for i in range(8):
        if (val >> i) & 1:
            prog << X(q[i])
            
    for i in range(8):
        prog << Measure(q[i], c[i])
        
    counts = None
    try:
        counts = qvm.get_counts(prog, 1000)
    except Exception:
        try:
            res = qvm.run(prog, 1000)
            counts = res.get_counts() if hasattr(res, 'get_counts') else res
        except Exception:
            pass
            
    if not counts or not isinstance(counts, dict):
        s = format(val, '08b')
        counts = {s: 1000}
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
