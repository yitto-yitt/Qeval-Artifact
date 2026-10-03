# EVAL_META: task_id=13, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def custom_rotation_gate():
    theta = np.pi / 2
    phi = np.pi / 2
    lam = np.pi / 2
    prog = QProg()
    prog << U4(theta, phi, lam, phi + lam, qubits[0])
    return prog

if __name__ == "__main__":
    prog = custom_rotation_gate()
    print(prog)
    machine.finalize()
