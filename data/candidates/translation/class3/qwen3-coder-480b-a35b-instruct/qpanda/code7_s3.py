# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import *

def create_parametrized_gate():
    theta = Parameter("theta")
    qvm = init_quantum_machine(QMachineType.CPU)
    q = qvm.qAlloc_many(1)
    prog = QProg()
    prog.insert(RX(q[0], theta))
    return prog
