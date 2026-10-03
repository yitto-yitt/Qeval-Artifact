# EVAL_META: task_id=54, framework=qpanda, class=1
import pyqpanda3.core as pq

def and_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q_a = machine.qAlloc_many(3)
    q_b = machine.qAlloc_many(3)
    ancillary = machine.qAlloc_many(3)
    measure = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2-i] == '1':
            prog << pq.X(q_a[i])
        if b_str[2-i] == '1':
            prog << pq.X(q_b[i])
            
    for i in range(3):
        prog << pq.Toffoli(q_a[i], q_b[i], ancillary[i])
        
    for i in range(3):
        prog << pq.Measure(ancillary[i], measure[i])
        
    result = machine.run_with_configuration(prog, measure[::-1], 1000)
    
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
