# EVAL_META: task_id=12, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QProg, H, CNOT, get_unitary as qp_get_unitary

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def get_unitary():
    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    u = qp_get_unitary(prog)
    mat = np.array(u).reshape(4, 4)
    return mat


if __name__ == "__main__":
    print(get_unitary())
    machine.finalize()
