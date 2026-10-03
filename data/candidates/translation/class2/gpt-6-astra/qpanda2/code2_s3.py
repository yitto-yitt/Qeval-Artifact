# EVAL_META: task_id=2, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QProg, H, CNOT


def create_bell_statevector():
    qvm = CPUQVM()
    qvm.init_qvm()
    try:
        qubits = qvm.qAlloc_many(2)
        program = QProg()
        program << H(qubits[0]) << CNOT(qubits[0], qubits[1])
        qvm.directly_run(program)
        return qvm.get_qstate()
    finally:
        qvm.finalize()
