# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq


def create_ghz(drawing=False):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.CNOT(q[0], q[2])

    prog << pq.MEASURE(q[0], c[0]) << pq.MEASURE(q[1], c[1]) << pq.MEASURE(
        q[2], c[2]
    )

    if drawing:
        try:
            draw = pq.draw_qprog(prog, "text")
        except:
            draw = pq.draw_qprog(prog)
        return prog, draw

    return prog
