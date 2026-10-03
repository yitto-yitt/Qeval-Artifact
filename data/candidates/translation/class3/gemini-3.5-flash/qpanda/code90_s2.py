# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import *

def create_custom_controlled():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qalloc_many(4)
    
    circuit = QCircuit()
    circuit << X(q[1]) << H(q[2])
    
    prog = QProg()
    prog << circuit.control([q[0], q[3]])
    return prog
