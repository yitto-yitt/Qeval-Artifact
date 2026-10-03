# EVAL_META: task_id=26, framework=qpanda, class=3
import pyqpanda3.core as pq


def bell_dag():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = pq.QProg()
    prog << pq.H(q[0])
    prog << pq.CNOT(q[0], q[1])
    prog << pq.Measure(q[0], c[0])

    dag = pq.qprog_to_dag(prog)
    return dag
