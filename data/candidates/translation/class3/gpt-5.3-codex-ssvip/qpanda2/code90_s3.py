# EVAL_META: task_id=90, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)
c = machine.cAlloc_many(4)

def create_custom_controlled():
    prog = pq.QProg()
    prog.insert(pq.X(q[1]).control([q[0], q[3]]))
    prog.insert(pq.H(q[2]).control([q[0], q[3]]))
    return prog

machine.finalize()
