# EVAL_META: task_id=39, framework=qpanda2, class=2
import pyqpanda as pq

def create_uniform_superposition(n):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n)
    prog = pq.QProg()
    for qubit in q:
        prog << pq.H(qubit)
    state = machine.get_qstate()
    machine.finalize()
    return state
