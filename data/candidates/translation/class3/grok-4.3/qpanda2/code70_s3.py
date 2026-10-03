# EVAL_META: task_id=70, framework=qpanda2, class=3
import pyqpanda as pq
machine = pq.CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(3)
def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    prog = pq.QProg()
    prog << pq.H(q[0])
    prog << pq.CSWAP(q[0], q[1], q[2])
    prog << pq.H(q[1])
    csdag = pq.controlled(pq.S(q[0]).dagger(), [q[1]])
    prog << csdag
    return prog
machine.finalize()
