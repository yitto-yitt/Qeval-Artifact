# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def circuit():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    
    prog = QProg()
    prog << H(q[0])
    
    # In pyQPanda3, we handle parameterized circuits differently
    # We'll create a template that can be used with different theta values
    def create_parametrized_circuit(theta_val):
        local_prog = QProg()
        local_prog << H(q[0]) << RZ(q[0], theta_val)
        return local_prog
    
    # Return the function that creates the parametrized circuit
    return create_parametrized_circuit
