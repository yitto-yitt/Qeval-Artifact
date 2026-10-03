# EVAL_META: task_id=2, framework=qpanda2, class=2
from pyqpanda import *
from pyqpanda.quantum_info import Statevector

def create_bell_statevector():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    qvm.run(prog)
    state = qvm.get_qstate()
    return Statevector(state)
