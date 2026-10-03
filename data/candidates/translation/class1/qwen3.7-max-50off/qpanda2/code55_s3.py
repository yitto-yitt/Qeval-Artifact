# EVAL_META: task_id=55, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def or_gate(a, b):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qr_a = machine.qAlloc_many(3)
    qr_b = machine.qAlloc_many(3)
    anc = machine.qAlloc_many(3)
    creg = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2-i] == '0':
            prog << pq.X(qr_a[i])
        if b_str[2-i] == '0':
            prog << pq.X(qr_b[i])
            
    for i in range(3):
        prog << pq.Toffoli(qr_a[i], qr_b[i], anc[i])
        prog << pq.X(anc[i])
        prog << pq.Measure(anc[i], creg[i])
        
    counts = machine.run_with_configuration(prog, creg, 1000)
    total = builtins.sum(counts.values())
    
    return {k: v / total for k, v in counts.items()}
