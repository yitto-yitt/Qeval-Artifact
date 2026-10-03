# EVAL_META: task_id=70, framework=qpanda2, class=3
import math
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    circ = QCircuit()
    circ << H(q[0])
    
    # CSWAP(0, 1, 2) decomposition
    circ << CNOT(q[2], q[1])
    circ << Toffoli(q[0], q[1], q[2])
    circ << CNOT(q[2], q[1])
    
    circ << H(q[1])
    
    # CSDG(1, 0) using Controlled-Phase
    circ << CP(q[1], q[0], -math.pi / 2)
    
    prog = QProg()
    prog.insert(circ)
    return prog

machine.finalize()
