# EVAL_META: task_id=26, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QProg, H, CNOT, Measure, qprog_to_dag

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)
c = machine.cAlloc_many(3)


def bell_dag():
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0])
    dag = qprog_to_dag(prog)
    return dag


machine.finalize()
