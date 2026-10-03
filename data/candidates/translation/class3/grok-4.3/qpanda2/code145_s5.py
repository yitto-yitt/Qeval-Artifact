# EVAL_META: task_id=145, framework=qpanda2, class=3
import pyqpanda as pq
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)
def qft_inverse(n):
    q = qubits[:n]
    circ = pq.QFT(q)
    return circ.dagger()
machine.finalize()
