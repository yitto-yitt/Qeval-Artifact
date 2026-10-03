# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import AllocateQubits, CNOT, H, QProg, prog_to_dag


def apply_op_back():
    q = AllocateQubits(3)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    dag = prog_to_dag(prog, q)

    final_prog = QProg()
    final_prog << H(q[0]) << CNOT(q[0], q[1]) << H(q[0])
    dag = prog_to_dag(final_prog, q)

    return dag
