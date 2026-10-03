# EVAL_META: task_id=3, framework=qpanda, class=2
import pyqpanda3.core as pq


def create_ghz(drawing=False):
    machine = pq.CPUQVM()
    machine.init_qvm()

    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = pq.QProg()
    prog << pq.H(q[0])
    prog << pq.CNOT(q[0], q[1])
    prog << pq.CNOT(q[0], q[2])
    prog << pq.Measure(q[0], c[0])
    prog << pq.Measure(q[1], c[1])
    prog << pq.Measure(q[2], c[2])

    if drawing:
        try:
            draw_result = pq.draw_qprog(prog)
        except Exception:
            draw_result = str(prog)
        return prog, draw_result

    return prog
