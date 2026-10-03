# EVAL_META: task_id=118, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QuantumMachine, QProg, U, T

def create_c3sx_circuit():
    qm = QuantumMachine()
    q = qm.qAlloc_many(4)
    prog = QProg()
    
    u_gate = U(q[3], np.pi/2, -np.pi/2, np.pi/2)
    cu_gate = u_gate.control([q[0], q[1], q[2]])
    prog << cu_gate
    
    t_gate = T(q[2])
    ct_gate = t_gate.control([q[0], q[1]])
    prog << ct_gate
    
    return prog
