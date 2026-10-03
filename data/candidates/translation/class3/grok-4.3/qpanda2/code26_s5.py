# EVAL_META: task_id=26, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(3)
c = machine.cAlloc_many(3)
def bell_dag():
    prog = create_empty_qprog()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0])
    dag = convert_qprog_to_dag(machine, prog)
    return dag
machine.finalize()
