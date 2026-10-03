# EVAL_META: task_id=2, framework=qpanda2, class=2
import pyqpanda as pq


def create_bell_statevector():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)

    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])

    qvm.directly_run(prog)
    statevector = qvm.get_qstate()
    qvm.finalize()

    return statevector
