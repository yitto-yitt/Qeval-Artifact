# EVAL_META: task_id=5, framework=qpanda2, class=2
from pyqpanda import *

def create_state_prep():
    machine = init_quantum_machine(QuantumMachineType.CPU)
    q = machine.qAlloc_many(2)
    prog = QProg()
    prog << X(q[0])
    return prog
