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
        machine << Toffoli(qr_a[i], qr_b[i], ancillary[i])
    
    for i in range(3):
        machine << X(ancillary[i])
    
    for i in range(3):
        machine << Measure(ancillary[i], c[i])
    
    result = machine << pq.QRunesToQProg(machine)
    machine.run()
    
    counts = machine.get_qstate()
    machine.finalize()
    
    # Get results from classical bits
    results_dict = {}
    for i in range(1000):  # Simulate multiple shots to get distribution
        machine = pq.CPUQVM()
        machine.init_qvm()
        qubits = machine.qAlloc_many(9)
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
            machine << Toffoli(qr_a[i], qr_b[i], ancillary[i])
        
        for i in range(3):
            machine << X(ancillary[i])
        
        for i in range(3):
            machine << Measure(ancillary[i], c[i])
        
        machine.run()
        
        bit_str = ""
        for j in range(3):
            bit_str += str(int(c[j]))
        
        if bit_str not in results_dict:
            results_dict[bit_str] = 0
        results_dict[bit_str] += 1
        
        machine.finalize()
    
    total = sum(results_dict.values())
    prob_dist = {key: value / total for key, value in results_dict.items()}
    
    return prob_dist
