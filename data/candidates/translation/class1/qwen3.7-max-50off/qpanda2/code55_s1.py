# EVAL_META: task_id=55, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def or_gate(a, b):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    
    qr_a = qvm.qAlloc_many(3)
    qr_b = qvm.qAlloc_many(3)
    ancillary = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)
    
    prog = pq.QProg()
    
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '0':
            prog << pq.X(qr_a[i])
        if b_bin[2-i] == '0':
            prog << pq.X(qr_b[i])
            
    for i in range(3):
        prog << pq.Toffoli(qr_a[i], qr_b[i], ancillary[i])
        
    for i in range(3):
        prog << pq.X(ancillary[i])
        
    for i in range(3):
        prog << pq.Measure(ancillary[i], c[i])
        
    result = qvm.run_with_configuration(prog, c, 1024)
    
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
