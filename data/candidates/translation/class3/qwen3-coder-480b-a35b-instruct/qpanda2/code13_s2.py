# EVAL_META: task_id=13, framework=qpanda2, class=3
import pyqpanda as pq
import math

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def custom_rotation_gate():
    prog = pq.QProg()
    theta = math.pi / 2
    phi = math.pi / 2
    lam = math.pi / 2
    
    prog.insert(pq.U(qubits[0], theta, phi, lam))
    return prog

machine.finalize()
