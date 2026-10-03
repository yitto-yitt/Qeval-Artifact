# EVAL_META: task_id=12, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def get_unitary():
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    mat = machine.get_unitary(prog)
    mat = np.array(mat)
    # Convert from QPanda big-endian to Qiskit little-endian by reversing qubit order
    mat = mat[[0, 2, 1, 3], :][:, [0, 2, 1, 3]]
    machine.finalize()
    return mat
