# EVAL_META: task_id=108, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np
from qiskit.quantum_info import Choi

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(16)

def to_unitary(data):
    if hasattr(data, '__class__') and data.__class__.__name__ in ['QProg', 'QCircuit', 'QGate', 'QDoubleGate', 'QSingleGate']:
        prog = pq.QProg()
        prog << data
        mat_flat = pq.get_matrix(prog)
        dim = int(np.sqrt(len(mat_flat)))
        matrix = np.array(mat_flat).reshape((dim, dim))
        n = int(np.log2(dim))
        if n > 1:
            matrix = matrix.reshape([2] * (2 * n))
            axes = list(range(n - 1, -1, -1)) + list(range(2 * n - 1, n - 1, -1))
            matrix = np.transpose(matrix, axes).reshape((dim, dim))
        return matrix
    return data

def initialize_adjoint_and_compose(data1, data2):
    data1_conv = to_unitary(data1)
    data2_conv = to_unitary(data2)
    choi1 = Choi(data1_conv)
    choi2 = Choi(data2_conv)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi

machine.finalize()
