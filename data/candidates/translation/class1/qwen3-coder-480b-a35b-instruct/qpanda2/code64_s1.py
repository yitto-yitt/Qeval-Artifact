# EVAL_META: task_id=64, framework=qpanda2, class=1
import pyqpanda as pq
from pyqpanda import *
import numpy as np


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    
    machine = init_quantum_machine(QMachineType.CPU)
    q_reg1 = machine.qAlloc_many(n)
    q_reg2 = machine.qAlloc_many(n)
    c_reg = machine.cAlloc_many(n)
    
    prog = QProg()
    
    # Apply Hadamard to first register
    for i in range(n):
        prog << H(q_reg1[i])
    
    prog << Barrier()
    
    # Apply CNOT gates between registers
    for i in range(n):
        prog << CNOT(q_reg1[i], q_reg2[i])
    
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(q_reg1[i], q_reg2[j])
        
        prog << Barrier()
        
        # Apply Hadamard to first register again
        for k in range(n):
            prog << H(q_reg1[k])
    
    # Measure the first register
    for l in range(n):
        prog << Measure(q_reg1[l], c_reg[l])
    
    return prog
