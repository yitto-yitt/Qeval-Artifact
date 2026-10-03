# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import *

def inv_circuit(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    prog = QProg()
    for i in range(2):
        prog << H(qubits[i+1])
    for i in range(2):
        prog << CNOT(qubits[i+1], qubits[i+3])
    return prog.dagger()
