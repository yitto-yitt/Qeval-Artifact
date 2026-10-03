# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import QProg, QVec, CVec, H, CNOT, Measure

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    
    q_reg1 = QVec(n)
    q_reg2 = QVec(n)
    c_reg = CVec(n)
    
    prog = QProg()
    
    for i in range(n):
        prog << H(q_reg1[i])
        
    for i in range(n):
        prog << CNOT(q_reg1[i], q_reg2[i])
        
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(q_reg1[i], q_reg2[j])
        for k in range(n):
            prog << H(q_reg1[k])
            
    for i in range(n):
        prog << Measure(q_reg1[i], c_reg[i])
        
    return prog
