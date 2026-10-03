# EVAL_META: task_id=2, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QProg, H, CNOT


def create_bell_statevector():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    qvm.directly_run(prog)
    state = qvm.get_qstate()
    qvm.finalize()
    return state
