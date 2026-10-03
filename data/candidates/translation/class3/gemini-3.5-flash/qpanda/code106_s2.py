# EVAL_META: task_id=106, framework=qpanda, class=3
import pyqpanda.core as pq


def compose_cnot_dihedral():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)

    prog = pq.QProg()

    # circ2 (applied first in compose: circ1.compose(circ2) -> circ2 then circ1)
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.T(q[0]))
    prog.insert(pq.X(q[1]))

    # circ1
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.T(q[0]))

    return prog
