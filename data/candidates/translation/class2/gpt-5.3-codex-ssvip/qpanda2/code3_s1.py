# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq


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
        drawer = pq.draw_qprog(prog, output="pic", filename="ghz_qpanda")
        return prog, drawer
    return prog
