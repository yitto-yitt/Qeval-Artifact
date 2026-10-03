# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QVec, CVec

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    
    q_reg1 = QVec(n)
    q_reg2 = QVec(n)
    c_reg = CVec(n)
    
    circ = QuantumCircuit()
    circ.insert(q_reg1)
    circ.insert(q_reg2)
    circ.insert(c_reg)
    
    for q in q_reg1:
        circ.h(q)
        
    circ.barrier()
    
    for i in range(n):
        circ.cx(q_reg1[i], q_reg2[i])
        
    if "1" in s:
        idx = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circ.cx(q_reg1[idx], q_reg2[j])
        circ.barrier()
        for q in q_reg1:
            circ.h(q)
            
    for i in range(n):
        circ.measure(q_reg1[i], c_reg[i])
        
    return circ
