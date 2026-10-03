# EVAL_META: task_id=27, framework=qpanda2, class=3
from pyqpanda import *
qvm = CPUQVM()
qvm.initQVM()
qubits = qvm.qAlloc_many(3)

def apply_op_back():
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << H(qubits[0])
    return prog

qvm.finalize()
