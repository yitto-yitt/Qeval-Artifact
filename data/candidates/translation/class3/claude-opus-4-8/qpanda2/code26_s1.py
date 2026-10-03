# EVAL_META: task_id=26, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)
c = machine.cAlloc_many(3)


def bell_dag():
    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << Measure(q[0], c[0])
    return prog


if __name__ == "__main__":
    dag = bell_dag()
    print(dag)
    machine.finalize()
