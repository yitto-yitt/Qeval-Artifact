# EVAL_META: task_id=54, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def and_gate(a, b):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    
    qr_a = machine.qAlloc_many(3)
    qr_b = machine.qAlloc_many(3)
    ancillary = machine.qAlloc_many(3)
    cr = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '1':
            prog << pq.X(qr_a[i])
        if b_bin[2-i] == '1':
            prog << pq.X(qr_b[i])
            
    for i in range(3):
        prog << pq.Toffoli(qr_a[i], qr_b[i], ancillary[i])
        
    for i in range(3):
        prog << pq.Measure(ancillary[i], cr[i])
        
    shots = 1024
    result = machine.run_with_configuration(prog, cr, shots)
    
    total = builtins.sum(result.values())
    
    return {key: value / total for key, value in result.items()}
