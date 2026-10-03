# EVAL_META: task_id=49, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QProg, H, CNOT

qvm = CPUQVM()
qvm.init_qvm()
qubits = qvm.qAlloc_many(2)

def simple_elitzur_vaidman():
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << H(qubits[0])
    return prog

qvm.finalize()
