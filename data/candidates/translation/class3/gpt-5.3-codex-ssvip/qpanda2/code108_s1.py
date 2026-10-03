# EVAL_META: task_id=108, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(1)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.array(data1, dtype=complex)
    choi2 = np.array(data2, dtype=complex)
    adjoint_choi1 = choi1.conj().T
    composed_choi = choi1 @ choi2
    machine.finalize()
    return choi1, adjoint_choi1, composed_choi
