# EVAL_META: task_id=106, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)


def compose_cnot_dihedral():
    prog1 = pq.QProg()
    prog1.insert(pq.CNOT(q[0], q[1]))
    prog1.insert(pq.T(q[0]))

    prog2 = pq.QProg()
    prog2.insert(pq.CNOT(q[0], q[1]))
    prog2.insert(pq.T(q[0]))
    prog2.insert(pq.X(q[1]))

    composed_prog = pq.QProg()
    composed_prog.insert(prog1)
    composed_prog.insert(prog2)
    return composed_prog


machine.finalize()
