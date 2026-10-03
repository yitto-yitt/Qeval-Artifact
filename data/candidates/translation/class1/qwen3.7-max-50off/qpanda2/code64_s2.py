# EVAL_META: task_id=64, framework=qpanda2, class=1
from pyqpanda import *

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    
    q_reg1 = alloc_qubits(n)
    q_reg2 = alloc_qubits(n)
    c_reg = alloc_cbits(n)
    
    prog = QProg()
    
    for q in q_reg1:
        prog << H(q)
        
    for i in range(n):
        prog << CNOT(q_reg1[i], q_reg2[i])
        
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(q_reg1[i], q_reg2[j])
                
        for q in q_reg1:
            prog << H(q)
            
    for i in range(n):
        prog << Measure(q_reg1[i], c_reg[i])
        
    return prog
