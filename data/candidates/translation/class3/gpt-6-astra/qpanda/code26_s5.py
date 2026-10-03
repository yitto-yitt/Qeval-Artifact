# EVAL_META: task_id=26, framework=qpanda, class=3
import pyqpanda3.core as pq


def bell_dag():
    prog = pq.QProg()
    prog << pq.H(0)
    prog << pq.CNOT(0, 1)
    prog << pq.measure(0, 0)

    for name in ("to_dag", "get_dag", "get_qprog_dag"):
        converter = getattr(prog, name, None)
        if callable(converter):
            return converter()

    for name in ("prog_to_dag", "qprog_to_dag"):
        converter = getattr(pq, name, None)
        if callable(converter):
            return converter(prog)

    dag_type = getattr(pq, "QProgDAG", None)
    if dag_type is not None:
        return dag_type(prog)

    return prog
