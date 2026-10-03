# EVAL_META: task_id=89, framework=qpanda2, class=3
from pyqpanda import *

qvm = CPUQVM()
qvm.init_qvm()
qubits = qvm.qAlloc_many(3)

def create_controlled_hgate():
    prog = QProg()
    prog << H(qubits[2]).control([qubits[0], qubits[1]])
    return prog

qvm.finalize()
