# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import *

def create_quantum_circuit_with_one_qubit_and_measure():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)
    prog = QProg()
    prog << Measure(q[0], c[0])
    return prog
