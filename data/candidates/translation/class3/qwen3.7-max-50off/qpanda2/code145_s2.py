# EVAL_META: task_id=145, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)

def qft_inverse(n):
    q = pq.QVec([qubits[i] for i in range(n)])
    return pq.QFT(q).dagger()

machine.finalize()
