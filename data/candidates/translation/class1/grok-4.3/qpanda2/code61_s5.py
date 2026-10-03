# EVAL_META: task_id=61, framework=qpanda2, class=1
from pyqpanda import *


def create_quantum_circuit_with_one_qubit_and_measure():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAllocMany(1)
    c = machine.cAllocMany(1)
    prog = QProg()
    prog << measure(q[0], c[0])
    return prog
