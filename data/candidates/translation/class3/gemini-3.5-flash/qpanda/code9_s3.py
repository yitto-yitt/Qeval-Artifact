# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import *

def create_efficientSU2():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    
    prog = QProg()
    
    # 12 parameters for Ry and Rz rotations
    params = [var(0.0) for _ in range(12)]
    
    # First rotation layer
    prog << RY(q[0], params[0]) << RZ(q[0], params[1])
    prog << RY(q[1], params[2]) << RZ(q[1], params[3])
    prog << RY(q[2], params[4]) << RZ(q[2], params[5])
    
    prog << BARRIER(q)
    
    # Entanglement layer (reverse_linear)
    prog << CNOT(q[2], q[1])
    prog << CNOT(q[1], q[0])
    
    prog << BARRIER(q)
    
    # Second rotation layer
    prog << RY(q[0], params[6]) << RZ(q[0], params[7])
    prog << RY(q[1], params[8]) << RZ(q[1], params[9])
    prog << RY(q[2], params[10]) << RZ(q[2], params[11])
    
    return prog
