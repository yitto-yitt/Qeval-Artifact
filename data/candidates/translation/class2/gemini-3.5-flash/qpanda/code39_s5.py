# EVAL_META: task_id=39, framework=qpanda, class=2
import pyqpanda3.core as pq

def create_uniform_superposition(n):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n)
    prog = pq.QProg()
    for qubit in q:
        prog << pq.H(qubit)
    machine.directly_run(prog)
    return machine.get_qstate()
