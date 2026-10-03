# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq

_QPANDA_KEEPALIVE = []


def create_ghz(drawing=False):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)

    ghz = pq.QProg()
    ghz << pq.H(q[0])
    ghz << pq.CNOT(q[0], q[1])
    ghz << pq.CNOT(q[0], q[2])
    ghz << pq.Measure(q[0], c[0])
    ghz << pq.Measure(q[1], c[1])
    ghz << pq.Measure(q[2], c[2])

    _QPANDA_KEEPALIVE.append((qvm, q, c))

    if drawing:
        try:
            drawing_obj = pq.draw_qprog(ghz, "pic")
        except Exception:
            try:
                drawing_obj = pq.draw_qprog(ghz, "text")
            except Exception:
                drawing_obj = str(ghz)
        return ghz, drawing_obj
    return ghz
