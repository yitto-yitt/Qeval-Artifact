# EVAL_META: task_id=54, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *
import math

def and_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    # Create quantum registers
    qubits_a = machine.qAlloc_many(3)
    qubits_b = machine.qAlloc_many(3)
    ancillary = machine.qAlloc_many(3)
    cbit = machine.cAlloc_many(3)
    
    # Initialize quantum program
    prog = pq.QProg()
    
    # Format inputs to binary strings
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    # Apply X gates based on input values
    for i in range(3):
        if a_bin[2-i] == '1':
            prog << X(qubits_a[i])
        if b_bin[2-i] == '1':
            prog << X(qubits_b[i])
    
    # Apply CCX (Toffoli) gates for AND operation
    for i in range(3):
        prog << Toffoli(qubits_a[i], qubits_b[i], ancillary[i])
    
    # Measure ancillary qubits
    for i in range(3):
        prog << Measure(ancillary[i], cbit[i])
    
    # Run the program
    result = machine.run_with_configuration(prog, cbit, 1024)
    
    # Process results
    counts = {}
    for res_str, count in result.items():
        # Reverse the string to match Qiskit's bit ordering
        reversed_str = res_str[::-1]
        if reversed_str in counts:
            counts[reversed_str] += count
        else:
            counts[reversed_str] = count
    
    total = sum(counts.values())
    prob_dist = {key: value / total for key, value in counts.items()}
    
    machine.finalize()
    
    return prob_dist
