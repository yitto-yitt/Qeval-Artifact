# EVAL_META: task_id=64, framework=qpanda2, class=1
import pyqpanda

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    
    q_reg1 = pyqpanda.qAlloc(n)
    q_reg2 = pyqpanda.qAlloc(n)
    c_reg = pyqpanda.cAlloc(n)
    
    prog = pyqpanda.QProg()
    
    for i in range(n):
        prog << pyqpanda.H(q_reg1[i])
        
    for i in range(n):
        prog << pyqpanda.CNOT(q_reg1[i], q_reg2[i])
        
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << pyqpanda.CNOT(q_reg1[i], q_reg2[j])
                
        for k in range(n):
            prog << pyqpanda.H(q_reg1[k])
            
    for i in range(n):
        prog << pyqpanda.Measure(q_reg1[i], c_reg[i])
        
    return prog
