# EVAL_META: task_id=61, framework=qpanda2, class=1
from pyqpanda import *

def create_quantum_circuit_with_one_qubit_and_measure():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAllocMany(1)
    c = qvm.cAllocMany(1)
    prog = QProg()
    prog << Measure(q[0], c[0])
    return prog
