# EVAL_META: task_id=9, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_efficientSU2():
    prog = pq.QProg()
    for i in range(3):
        prog << pq.RY(q[i], 0.0)
        prog << pq.RZ(q[i], 0.0)
    prog << pq.BARRIER(q)
    prog << pq.CNOT(q[0], q[1])
    prog << pq.CNOT(q[1], q[2])
    prog << pq.BARRIER(q)
    for i in range(3):
        prog << pq.RY(q[i], 0.0)
        prog << pq.RZ(q[i], 0.0)
    return prog

machine.finalize()
