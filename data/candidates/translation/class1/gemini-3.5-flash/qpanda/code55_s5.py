# EVAL_META: task_id=55, framework=qpanda, class=1
import pyqpanda3.core as pq

def or_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(9)
    prog = pq.QProg()
    
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2-i] == '0':
            prog << pq.X(q[i])
        if b_str[2-i] == '0':
            prog << pq.X(q[3+i])
            
    for i in range(3):
        controls = pq.QVec()
        controls.append(q[i])
        controls.append(q[3+i])
        prog << pq.X(q[6+i]).control(controls)
        
    prog << pq.X(q[6])
    prog << pq.X(q[7])
    prog << pq.X(q[8])
    
    measure_qubits = pq.QVec()
    measure_qubits.append(q[8])
    measure_qubits.append(q[7])
    measure_qubits.append(q[6])
    
    res = machine.prob_run_dict(prog, measure_qubits)
    
    return {k: v for k, v in res.items() if v > 0.0}
