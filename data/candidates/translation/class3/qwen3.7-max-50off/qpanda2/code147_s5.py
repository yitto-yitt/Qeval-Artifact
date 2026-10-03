# EVAL_META: task_id=147, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)

def mcy(qc):
    if qc is None:
        qc = pq.QProg()
    gate = pq.Y(q[4])
    mc_gate = gate.control([q[0], q[1], q[2], q[3]])
    qc << mc_gate
    return qc

prog = mcy(pq.QProg())
machine.finalize()
