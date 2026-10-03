# EVAL_META: task_id=44, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init()
qubits = machine.qAlloc_many(3)

def tensor_circuits():
    prog = pq.QProg()
    prog << pq.CRY(qubits[0], qubits[1], 0.2)
    prog << pq.X(qubits[2])
    return prog

machine.finalize()
