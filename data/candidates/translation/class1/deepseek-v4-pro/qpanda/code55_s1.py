# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import *

def or_gate(a, b):
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    qvm = QVM()
    qvm.init()
    
    qubits = qvm.qAlloc_many(9)
    cbits = qvm.cAlloc_many(3)
    qr_a = qubits[0:3]
    qr_b = qubits[3:6]
    anc = qubits[6:9]
    
    prog = QProg()
    
    # Encode complement of input bits
    for i in range(3):
        if a_str[2 - i] == '0':
            prog << X(qr_a[i])
        if b_str[2 - i] == '0':
            prog << X(qr_b[i])
    
    # Toffoli gates to compute NOR, then flip with X to get OR
    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], anc[i])
    
    # Flip ancillary to obtain OR results
    for i in range(3):
        prog << X(anc[i])
    
    # Measure ancillary to classical bits
    for i in range(3):
        prog << Measure(anc[i], cbits[i])
    
    shots = 1024
    result = qvm.run_with_configuration(prog, cbits, shots)
    
    total = sum(result.values())
    distribution = {key: value / total for key, value in result.items()}
    
    qvm.stop()
    return distribution
