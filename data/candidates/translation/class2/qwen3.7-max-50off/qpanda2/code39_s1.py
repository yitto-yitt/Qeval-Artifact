# EVAL_META: task_id=39, framework=qpanda2, class=2
import pyqpanda as pq

def create_uniform_superposition(n):
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = qvm.qAlloc_many(n)
    prog = pq.QProg()
    for q in qubits:
        prog << pq.H(q)
    qvm.run(prog)
    return qvm.get_qstate()
