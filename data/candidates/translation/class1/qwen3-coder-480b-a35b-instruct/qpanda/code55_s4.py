# EVAL_META: task_id=55, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *
import math

def or_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(9)  # 3 for a, 3 for b, 3 for ancillary
    cbits = machine.cAlloc_many(3)   # 3 classical bits for measurement
    
    qr_a = qubits[:3]
    qr_b = qubits[3:6]
    ancillary = qubits[6:9]
    measure = cbits
    
    prog = pq.QProg()
    
    # Format inputs to 3-bit binary strings
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    # Apply X gates based on input values (inverting 0s)
    for i in range(3):
        if a_str[2-i] == '0':
            prog.insert(pq.X(qr_a[i]))
        if b_str[2-i] == '0':
            prog.insert(pq.X(qr_b[i]))
    
    # Apply CCX (Toffoli) gates for AND operation
    for i in range(3):
        prog.insert(pq.TOFFOLI(qr_a[i], qr_b[i], ancillary[i]))
    
    # Apply X gates to ancillary to get OR result (since NOT(AND(NOT(a), NOT(b))) = OR)
    for i in range(3):
        prog.insert(pq.X(ancillary[i]))
    
    # Measure ancillary qubits
    for i in range(3):
        prog.insert(pq.Measure(ancillary[i], measure[i]))
    
    result = machine.run_with_configuration(prog, measure, 1024)
    
    # Convert results to probability distribution
    total_shots = sum(result.values())
    prob_dist = {}
    for outcome, count in result.items():
        # Reverse the bit string to match expected order
        reversed_outcome = outcome[::-1]
        prob_dist[reversed_outcome] = count / total_shots
    
    machine.finalize()
    return prob_dist
