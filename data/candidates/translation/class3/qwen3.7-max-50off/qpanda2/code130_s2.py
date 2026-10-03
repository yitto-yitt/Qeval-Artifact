# EVAL_META: task_id=130, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(100)

def inv_circuit(n):
    prog = pq.QProg()
    prog.insert(pq.CNOT(q[2], q[4]))
    prog.insert(pq.CNOT(q[1], q[3]))
    prog.insert(pq.H(q[2]))
    prog.insert(pq.H(q[1]))
    return prog

machine.finalize()
