# EVAL_META: task_id=2, framework=qpanda2, class=2
import pyqpanda as pq


def create_bell_statevector():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    try:
        qubits = qvm.qAlloc_many(2)
        program = pq.QProg()
        program << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
        qvm.directly_run(program)
        return qvm.get_qstate()
    finally:
        qvm.finalize()
