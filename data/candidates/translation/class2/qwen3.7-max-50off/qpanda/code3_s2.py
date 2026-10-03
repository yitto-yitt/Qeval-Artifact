# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QProg, Qubit, CBit, H, CNOT, Measure

def create_ghz(drawing=False):
    prog = QProg()
    q = [Qubit() for _ in range(3)]
    c = [CBit() for _ in range(3)]
    
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << CNOT(q[0], q[2])
    
    for i in range(3):
        prog << Measure(q[i], c[i])
        
    if drawing:
        try:
            return prog, prog.draw()
        except Exception:
            return prog, None
    return prog
