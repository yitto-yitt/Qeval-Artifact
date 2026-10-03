# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QProg, QCircuit

def or_gate(a, b):
    qm = QuantumMachine()
    qr_a = [qm.qAlloc() for _ in range(3)]
    qr_b = [qm.qAlloc() for _ in range(3)]
    ancillary = [qm.qAlloc() for _ in range(3)]
    
    prog = QProg()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '0':
            prog << QCircuit.X(qr_a[i])
        if b_bin[2-i] == '0':
            prog << QCircuit.X(qr_b[i])
            
    for i in range(3):
        prog << QCircuit.X(ancillary[i]).control([qr_a[i], qr_b[i]])
        prog << QCircuit.X(ancillary[i])
        
    result = qm.prob_run_dict(prog, [ancillary[0], ancillary[1], ancillary[2]])
    return result
