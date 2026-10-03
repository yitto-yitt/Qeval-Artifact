# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import *

def create_swap_gate():
    qvm = init_quantum_machine(QMachineType.CPU)
    q = qvm.qAlloc_many(2)
    prog = QProg()
    prog.insert(CNOT(q[0], q[1])).insert(CNOT(q[1], q[0])).insert(CNOT(q[0], q[1]))
    return prog
