# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import *

def create_cy_gate():
    qvm = init_quantum_machine(QMachineType.CPU)
    q = qvm.qAlloc_many(2)
    prog = QProg()
    
    prog << S(q[1]).dagger() << CNOT(q[0], q[1]) << S(q[1])
    
    return prog
