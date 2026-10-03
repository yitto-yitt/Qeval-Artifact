# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda import *
from collections import defaultdict

def and_gate(a, b):
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    
    machine = init(QMachineType.CPU)
    prog = QProg()
    
    qr_a = [machine.qAlloc() for _ in range(3)]
    qr_b = [machine.qAlloc() for _ in range(3)]
    ancillary = [machine.qAlloc() for _ in range(3)]
    measure = [machine.cAlloc() for _ in range(3)]
    
    for i in range(3):
        if a_bits[2-i] == '1':
            prog.insert(X(qr_a[i]))
        if b_bits[2-i] == '1':
            prog.insert(X(qr_b[i]))
            
    for i in range(3):
        prog.insert(Toffoli(qr_a[i], qr_b[i], ancillary[i]))
        
    for i in range(3):
        prog.insert(Measure(ancillary[i], measure[i]))
        
    result = machine.run_with_configuration(prog, list(measure), 8192)
    counts = defaultdict(int)
    for key, value in result.items():
        counts[key[::-1]] += value
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
