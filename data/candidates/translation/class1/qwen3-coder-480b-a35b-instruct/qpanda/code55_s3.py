# EVAL_META: task_id=55, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *
import math

def or_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(9)  # 3 for a, 3 for b, 3 for ancillary
    c = machine.cAlloc_many(3)
    
    qr_a = qubits[:3]
    qr_b = qubits[3:6]
    ancillary = qubits[6:9]
    
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    
    for i in range(3):
        if a_bits[2-i] == '0':
            machine << X(qr_a[i])
        if b_bits[2-i] == '0':
            machine << X(qr_b[i])
    
    for i in range(3):
        machine << CCX(qr_a[i], qr_b[i], ancillary[i])
    
    machine << X(ancillary[0]) << X(ancillary[1]) << X(ancillary[2])
    
    prog = pq.QProg()
    for i in range(3):
        prog << Measure(ancillary[i], c[i])
    
    result = machine << prog
    prob = machine.prob_run_dict(prog, c)
    
    machine.finalize()
    
    return prob
