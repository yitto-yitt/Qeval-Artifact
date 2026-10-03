# EVAL_META: task_id=147, framework=qpanda2, class=3
import pyqpanda as pq

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def mcy(qc):
    gate = pq.Y(qubits[4]).control(qubits[0:4])
    qc << gate
    return qc

# Manual Cleanup
machine.finalize()
