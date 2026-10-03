# EVAL_META: task_id=9, framework=qpanda, class=3
import sympy
from pyqpanda3.core import QProg, QVec, RY, RZ, CNOT

def create_efficientSU2():
    qvec = QVec(3)
    prog = QProg()
    params = sympy.symbols('theta0:12')
    
    idx = 0
    for i in range(3):
        prog << RY(qvec[i], params[idx])
        prog << RZ(qvec[i], params[idx+1])
        idx += 2
        
    prog << CNOT(qvec[0], qvec[1])
    prog << CNOT(qvec[1], qvec[2])
    
    for i in range(3):
        prog << RY(qvec[i], params[idx])
        prog << RZ(qvec[i], params[idx+1])
        idx += 2
        
    return prog
