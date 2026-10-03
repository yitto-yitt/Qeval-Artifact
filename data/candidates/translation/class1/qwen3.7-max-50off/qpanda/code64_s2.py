# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import QProg, QVec, H, CX, Measure

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    
    q1 = QVec(n)
    q2 = QVec(n)
    
    prog = QProg()
    
    for i in range(n):
        prog << H(q1[i])
        
    for i in range(n):
        prog << CX(q1[i], q2[i])
        
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CX(q1[i], q2[j])
        for k in range(n):
            prog << H(q1[k])
            
    for i in range(n):
        prog << Measure(q1[i])
        
    return prog
