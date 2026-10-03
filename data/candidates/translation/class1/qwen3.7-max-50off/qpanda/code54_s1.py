# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QProg, X, Toffoli, Measure

def and_gate(a, b):
    qm = QuantumMachine()
    qr_a = qm.qAlloc_many(3)
    qr_b = qm.qAlloc_many(3)
    anc = qm.qAlloc_many(3)
    cr = qm.cAlloc_many(3)
    
    prog = QProg()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '1':
            prog << X(qr_a[i])
        if b_bin[2-i] == '1':
            prog << X(qr_b[i])
            
    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], anc[i])
        
    for i in range(3):
        prog << Measure(anc[i], cr[i])
        
    counts = qm.run_with_configuration(prog, cr, 1000)
    total = sum(counts.values())
    
    result = {}
    for k, v in counts.items():
        if isinstance(k, int):
            k = format(k, '03b')
        if len(k) < 3:
            k = k.zfill(3)
        result[k] = v / total
        
    return result
