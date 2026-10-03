# EVAL_META: task_id=26, framework=qpanda2, class=3
import pyqpanda as pq

# Initialize global QVM
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)
c = machine.cAlloc_many(3)


def bell_dag():
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.Measure(q[0], c[0])
    dag = pq.qprog_to_dag(prog)
    return dag


machine.finalize()
