# EVAL_META: task_id=39, framework=qpanda, class=2
import pyqpanda3.core as pq

def create_uniform_superposition(n):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    prog = pq.QProg()
    for q in qubits:
        prog << pq.H(q)
    qvm.directly_run(prog)
    return qvm.get_qstate()
