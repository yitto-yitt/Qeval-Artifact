# EVAL_META: task_id=26, framework=qpanda2, class=3
from pyqpanda import *

qvm = CPUQVM()
qvm.init_qvm()
qubits = qvm.qAlloc_many(3)
cbits = qvm.cAlloc_many(3)

def bell_dag():
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << Measure(qubits[0], cbits[0])
    return prog

qvm.finalize()
