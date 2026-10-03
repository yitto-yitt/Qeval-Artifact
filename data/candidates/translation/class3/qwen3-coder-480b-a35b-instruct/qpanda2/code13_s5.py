# EVAL_META: task_id=13, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def custom_rotation_gate():
    prog = pq.QProg()
    theta = np.pi / 2
    phi = np.pi / 2
    lam = np.pi / 2
    prog.insert(pq.U(theta, phi, lam, qubits[0]))
    return prog

machine.finalize()
