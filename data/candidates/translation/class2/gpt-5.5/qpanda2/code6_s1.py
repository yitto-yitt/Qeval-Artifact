# EVAL_META: task_id=6, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep(num_qubits):
    try:
        pq.init()
    except Exception:
        pass

    qubits = pq.qAlloc_many(num_qubits)
    prog = pq.QProg()

    if num_qubits > 0:
        prog.insert(pq.X(qubits[0]))
        for i in range(1, num_qubits):
            prog.insert(pq.I(qubits[i]))

    return prog
