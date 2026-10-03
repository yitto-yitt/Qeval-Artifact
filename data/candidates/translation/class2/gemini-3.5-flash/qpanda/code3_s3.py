# EVAL_META: task_id=3, framework=qpanda, class=2
import pyqpanda3.core as pq


def create_ghz(drawing=False):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.CNOT(q[0], q[2])

    for i in range(3):
        prog << pq.Measure(q[i], c[i])

    if drawing:
        try:
            draw_result = pq.draw_qprog(prog)
        except Exception:
            draw_result = None
        return prog, draw_result
    return prog
