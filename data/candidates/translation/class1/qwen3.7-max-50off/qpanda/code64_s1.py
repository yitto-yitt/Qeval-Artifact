# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import QMachine, QProg, QCircuit, H, CX, Measure, Barrier

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    qm = QMachine()
    q_reg1 = qm.alloc_qubits(n)
    q_reg2 = qm.alloc_qubits(n)
    c_reg = qm.alloc_cbits(n)
    
    prog = QProg()
    circ = QCircuit()
    
    circ << H(q_reg1)
    circ << Barrier(q_reg1)
    circ << Barrier(q_reg2)
    circ << CX(q_reg1, q_reg2)
    
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circ << CX(q_reg1[i], q_reg2[j])
        circ << Barrier(q_reg1)
        circ << Barrier(q_reg2)
        circ << H(q_reg1)
        
    prog << circ
    prog << Measure(q_reg1, c_reg)
    
    return prog
