# EVAL_META: task_id=54, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def and_gate(a, b):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(9)
    c = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2-i] == '1':
            prog << pq.X(q[i])
        if b_str[2-i] == '1':
            prog << pq.X(q[3+i])
            
    for i in range(3):
        prog << pq.Toffoli(q[i], q[3+i], q[6+i])
        
    for i in range(3):
        prog << pq.Measure(q[6+i], c[i])
        
    shots = 1000
    result = machine.run_with_configuration(prog, c, shots)
    
    total = builtins.sum(result.values())
    prob_dist = {key: val / total for key, val in result.items()}
    
    pq.destroy_quantum_machine(machine)
    return prob_dist
