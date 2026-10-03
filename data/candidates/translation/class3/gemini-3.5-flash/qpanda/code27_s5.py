# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import CNOT, H, CPUAllocator, QProg, qprog_to_dag


def apply_op_back():
    machine = CPUAllocator()
    q = machine.qAlloc_many(3)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    prog << H(q[0])
    dag = qprog_to_dag(prog)
    return dag
