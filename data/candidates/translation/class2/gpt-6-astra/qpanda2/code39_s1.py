# EVAL_META: task_id=39, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QProg, H

def create_uniform_superposition(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    try:
        qubits = qvm.qAlloc_many(n)
        program = QProg()
        for qubit in qubits:
            program << H(qubit)
        qvm.directly_run(program)
        return qvm.get_qstate()
    finally:
        qvm.finalize()
