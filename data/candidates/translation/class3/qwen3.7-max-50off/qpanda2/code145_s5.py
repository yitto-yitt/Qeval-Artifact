# EVAL_META: task_id=145, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(64)

def qft_inverse(n):
    qubits = pq.QVec([q[i] for i in range(n)])
    circ = pq.QFT(qubits)
    return circ.dagger()

machine.finalize()
