# EVAL_META: task_id=54, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def and_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(9)
    c = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2-i] == '1':
            prog << pq.X(q[i])
        if b_str[2-i] == '1':
            prog << pq.X(q[i+3])
            
    for i in range(3):
        prog << pq.X(q[i+6]).control([q[i], q[i+3]])
        
    for i in range(3):
        prog << pq.Measure(q[i+6], c[i])
        
    shots = 1000
    counts = machine.run_with_configuration(prog, c, shots)
    
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
