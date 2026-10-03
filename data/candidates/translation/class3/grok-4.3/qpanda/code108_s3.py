# EVAL_META: task_id=108, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, H, CNOT
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog.insert(H(qubits[0])).insert(CNOT(qubits[0], qubits[1]))
    qvm.run_with_configuration(prog, qubits, 1024)
    choi1 = np.asarray(data1, dtype=complex)
    choi2 = np.asarray(data2, dtype=complex)
    adjoint_choi1 = choi1.conj().T
    composed_choi = choi1 @ choi2
    qvm.finalize()
    return choi1, adjoint_choi1, composed_choi
