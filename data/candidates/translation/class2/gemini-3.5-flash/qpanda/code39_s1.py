# EVAL_META: task_id=39, framework=qpanda, class=2
import pyqpanda3.core as pq

def create_uniform_superposition(n):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qlist = machine.qAllocMany(n)
    prog = pq.QProg()
    for q in qlist:
        prog << pq.H(q)
    machine.directly_run(prog)
    return machine.get_qstate()
