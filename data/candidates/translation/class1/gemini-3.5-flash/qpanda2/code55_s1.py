# EVAL_META: task_id=55, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def or_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(9)
    qr_a = q[0:3]
    qr_b = q[3:6]
    ancillary = q[6:9]
    
    c = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2-i] == '0':
            prog << pq.X(qr_a[i])
        if b_str[2-i] == '0':
            prog << pq.X(qr_b[i])
            
    for i in range(3):
        prog << pq.Toffoli(qr_a[i], qr_b[i], ancillary[i])
        
    for i in range(3):
        prog << pq.X(ancillary[i])
        
    for i in range(3):
        prog << pq.Measure(ancillary[i], c[i])
        
    shots = 1000
    result = machine.run_with_configuration(prog, c, shots)
    
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
