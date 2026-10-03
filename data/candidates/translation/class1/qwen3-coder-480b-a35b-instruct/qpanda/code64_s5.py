# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import *
import numpy as np

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    
    machine = CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(2 * n)
    q_reg1 = qubits[:n]
    q_reg2 = qubits[n:]
    cbits = machine.cAlloc_many(n)
    
    prog = QProg()
    
    # Apply Hadamard to first register
    for qubit in q_reg1:
        prog << H(qubit)
    
    # Add barrier
    prog << Barrier()
    
    # Apply CNOT gates between registers
    for i in range(n):
        prog << CNOT(q_reg1[i], q_reg2[i])
    
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(q_reg1[i], q_reg2[j])
        
        # Add barrier
        prog << Barrier()
        
        # Apply Hadamard to first register again
        for qubit in q_reg1:
            prog << H(qubit)
    
    # Measure first register
    for i in range(n):
        prog << Measure(q_reg1[i], cbits[i])
    
    return prog
