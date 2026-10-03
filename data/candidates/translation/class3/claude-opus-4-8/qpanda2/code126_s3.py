# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, qAlloc_many, H, matrix_decompose, QProgDAGVertex
from pyqpanda.Visualization.circuit_draw import draw_qprog
from pyqpanda.utils import matrix_to_unitary

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def calculate_phase_difference_fidelity():
    h_matrix = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    op_a = h_matrix
    op_b = np.exp(1j * 0.5) * h_matrix
    
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b)) / 2
    
    return fidelity


machine.finalize()
