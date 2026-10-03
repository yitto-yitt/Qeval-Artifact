# EVAL_META: task_id=5, framework=qpanda2, class=2
from pyqpanda import *

def create_state_prep():
    machine = init_quantum_machine(QMachineType.CPU)
    qlist = machine.qAlloc_many(2)
    prog = create_empty_qprog()
    prog << X(qlist[0])
    return prog
