# EVAL_META: task_id=44, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def tensor_circuits():
    prog = pq.QProg()
    prog.insert(pq.CRY(q[0], q[1], 0.2))
    prog.insert(pq.X(q[2]))
    machine.directly_run(prog)
    return prog

machine.finalize()
