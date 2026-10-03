# EVAL_META: task_id=38, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    prog = pq.QProg()
    prog << pq.H(q[0])
    prog << pq.RZ(q[1], theta).control([q[0]])
    prog << pq.H(q[1])
    prog << pq.RY(q[0], theta).control([q[1]])
    return prog

machine.finalize()
