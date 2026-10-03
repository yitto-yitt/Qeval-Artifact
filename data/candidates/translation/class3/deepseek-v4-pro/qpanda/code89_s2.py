# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import QProg, qAlloc_many, H, init_quantum_machine, QMachineType

def create_controlled_hgate():
    init_quantum_machine(QMachineType.CPU)
    q = qAlloc_many(3)
    prog = QProg()
    prog << H(q[2]).control([q[0], q[1]])
    return prog
