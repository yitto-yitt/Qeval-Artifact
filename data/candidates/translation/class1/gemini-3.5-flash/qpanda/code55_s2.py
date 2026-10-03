# EVAL_META: task_id=55, framework=qpanda, class=1
import pyqpanda3.core as pq

def or_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(9)
    c = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2-i] == '0':
            prog << pq.X(q[i])
        if b_str[2-i] == '0':
            prog << pq.X(q[3+i])
            
    for i in range(3):
        prog << pq.Toffoli(q[i], q[3+i], q[6+i])
        
    for i in range(3):
        prog << pq.X(q[6+i])
        
    for i in range(3):
        prog << pq.Measure(q[6+i], c[i])
        
    result = machine.run_with_configuration(prog, c, 1000)
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
