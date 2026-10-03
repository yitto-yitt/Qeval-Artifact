# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda3.core import *

def convert_qasm_string_to_quantum_circuit():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    return prog
