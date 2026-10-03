# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def and_gate(a, b):
    qm = QMachine()
    qr_a = qm.qAlloc_many(3)
    qr_b = qm.qAlloc_many(3)
    ancillary = qm.qAlloc_many(3)
    measure = qm.cAlloc_many(3)
    
    circ = QuantumCircuit()
    
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '1':
            circ.x(qr_a[i])
        if b_bin[2-i] == '1':
            circ.x(qr_b[i])
            
    for i in range(3):
        circ.ccx(qr_a[i], qr_b[i], ancillary[i])
        
    for i in range(3):
        circ.measure(ancillary[i], measure[i])
        
    prob_dict = qm.prob_run_dict(circ, measure)
    return prob_dict
