# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import *

def create_bell_statevector():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)

    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])

    qvm.directly_run(prog)
    return qvm.get_qstate()
