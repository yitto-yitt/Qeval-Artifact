# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import *

def create_custom_controlled():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(4)
    
    prog = QProg()
    cir = QCircuit()
    cir << X(q[1]) << H(q[2])
    
    controlled_cir = cir.control([q[0], q[3]])
    prog << controlled_cir
    return prog
