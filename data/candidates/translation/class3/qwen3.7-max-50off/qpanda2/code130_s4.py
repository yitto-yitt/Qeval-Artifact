# EVAL_META: task_id=130, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(256)

def inv_circuit(n):
    q = qubits[:n]
    prog = pq.QProg()
    for i in range(2):
        prog << pq.H(q[i+1])
    for i in range(2):
        prog << pq.CNOT(q[i+1], q[i+3])
    return prog.dagger()

machine.finalize()
