# EVAL_META: task_id=145, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(128)

def qft_inverse(n):
    qubits = q[:n]
    return pq.QFT(qubits).dagger()

machine.finalize()
