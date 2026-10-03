# EVAL_META: task_id=61, framework=qpanda2, class=1
from pyqpanda import *
import builtins


def create_quantum_circuit_with_one_qubit_and_measure():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)
    prog = QProg()
    prog << measure(q[0], c[0])
    return prog
