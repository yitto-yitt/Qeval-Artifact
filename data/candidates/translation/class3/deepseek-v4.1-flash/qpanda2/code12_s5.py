# EVAL_META: task_id=12, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def get_unitary():
    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    mat = machine.get_unitary(prog)
    U = np.array(mat, dtype=complex)
    P = np.array([[1,0,0,0],
                  [0,0,1,0],
                  [0,1,0,0],
                  [0,0,0,1]], dtype=complex)
    return P @ U @ P

if __name__ == "__main__":
    machine.finalize()
