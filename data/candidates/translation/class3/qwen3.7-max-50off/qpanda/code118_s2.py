# EVAL_META: task_id=118, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, U3, U1

def create_c3sx_circuit():
    qc = QCircuit()
    q = [qc.allocate_qubit() for _ in range(4)]
    
    # SX gate is equivalent to e^{i*pi/4} * U3(pi/2, -pi/2, pi/2)
    # Therefore, C3SX is equivalent to C3(U3) * C3(U1(pi/4))
    u3_gate = U3(np.pi/2, -np.pi/2, np.pi/2)(q[3]).control([q[0], q[1], q[2]])
    u1_gate = U1(np.pi/4)(q[3]).control([q[0], q[1], q[2]])
    
    qc << u3_gate
    qc << u1_gate
    
    return qc
