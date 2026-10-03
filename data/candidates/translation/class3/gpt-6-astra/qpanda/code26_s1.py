# EVAL_META: task_id=26, framework=qpanda, class=3
import pyqpanda3.core as pq


def bell_dag():
    prog = pq.QProg()
    prog << pq.I(2)
    prog << pq.H(0)
    prog << pq.CNOT(0, 1)
    prog << pq.measure(0, 0)

    to_dag = getattr(pq, "prog_to_dag", None)
    if callable(to_dag):
        return to_dag(prog)
    return prog
