# EVAL_META: task_id=55, framework=qpanda, class=1
import pyqpanda3.core as pq

def or_gate(a, b):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    
    qv = qvm.qAlloc_many(9)
    qr_a = qv[0:3]
    qr_b = qv[3:6]
    ancillary = qv[6:9]
    
    prog = pq.QProg()
    
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2-i] == '0':
            prog.insert(pq.X(qr_a[i]))
        if b_str[2-i] == '0':
            prog.insert(pq.X(qr_b[i]))
            
    for i in range(3):
        prog.insert(pq.TOFFOLI(qr_a[i], qr_b[i], ancillary[i]))
        
    for i in range(3):
        prog.insert(pq.X(ancillary[i]))
        
    result_qubits = [ancillary[2], ancillary[1], ancillary[0]]
    result = qvm.prob_run_dict(prog, result_qubits, -1)
    
    return result
