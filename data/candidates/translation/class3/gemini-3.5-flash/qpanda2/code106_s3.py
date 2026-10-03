# EVAL_META: task_id=106, framework=qpanda2, class=3
import pyqpanda as pq

# Initialize Global QVM
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def compose_cnot_dihedral():
    prog = pq.QProg()
    prog << pq.CNOT(q[0], q[1])
    prog << pq.T(q[0])
    prog << pq.CNOT(q[0], q[1])
    prog << pq.T(q[0])
    prog << pq.X(q[1])
    return prog

machine.finalize()
