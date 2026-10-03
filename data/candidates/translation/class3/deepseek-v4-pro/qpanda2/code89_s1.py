# EVAL_META: task_id=89, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_controlled_hgate():
    circuit = QProg()
    circuit << H(q[2]).control([q[0], q[1]])
    return circuit

machine.finalize()
