# EVAL_META: task_id=10, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
cbits = machine.cAlloc_many(2)

def create_operator():
    prog = pq.QProg()
    prog << pq.X(qubits[0]) << pq.X(qubits[1])
    return prog

machine.finalize()
