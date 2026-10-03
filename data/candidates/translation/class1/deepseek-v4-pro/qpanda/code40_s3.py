# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import init, finalize, QVM, QProg, Measure

def init_random_3qubit(desired_vector):
    init()
    try:
        qvm = QVM()
        q = qvm.qAlloc_many(3)
        c = qvm.cAlloc_many(3)
        try:
            qvm.set_seed(42)
        except AttributeError:
            pass
        qvm.init_vector(desired_vector, q)
        prog = QProg()
        for i in range(3):
            prog << Measure(q[i], c[i])
        counts = qvm.run_with_configuration(prog, c, 1024)
        total = sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        finalize()
