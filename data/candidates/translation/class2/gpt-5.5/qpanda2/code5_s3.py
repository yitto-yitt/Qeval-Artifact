# EVAL_META: task_id=5, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep():
    try:
        pq.init()
    except Exception:
        pass

    qubits = pq.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.X(qubits[0])
    return prog
