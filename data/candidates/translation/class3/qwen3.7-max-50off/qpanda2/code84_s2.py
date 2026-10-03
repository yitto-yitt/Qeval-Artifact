# EVAL_META: task_id=84, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def controlled_custom_unitary_circuit():
    theta, phi, lam = 0.3, 0.2, 0.1
    
    prog = pq.QProg()
    prog << pq.U1(q[0], (lam + phi) / 2)
    prog << pq.U1(q[1], (lam - phi) / 2)
    prog << pq.CNOT(q[0], q[1])
    prog << pq.U3(q[1], -theta / 2, 0, -(phi + lam) / 2)
    prog << pq.CNOT(q[0], q[1])
    prog << pq.U3(q[1], theta / 2, phi, 0)
    
    return prog

machine.finalize()
