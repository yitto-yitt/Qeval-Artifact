# EVAL_META: task_id=126, framework=qpanda2, class=3
import atexit
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def calculate_phase_difference_fidelity():
    try:
        h_matrix = np.array(H(qubits[0]).get_matrix(), dtype=complex)
    except Exception:
        try:
            h_matrix = np.array(get_matrix(H(qubits[0])), dtype=complex)
        except Exception:
            columns = []
            for bit in (0, 1):
                prog = QProg()
                try:
                    prog << Reset(qubits[0])
                except Exception:
                    pass
                if bit:
                    prog << X(qubits[0])
                prog << H(qubits[0])
                machine.directly_run(prog)
                columns.append(np.array(machine.get_qstate(), dtype=complex)[:2])
            h_matrix = np.column_stack(columns)

    if h_matrix.shape != (2, 2):
        h_matrix = h_matrix.reshape((2, 2))

    op_a = h_matrix
    op_b = np.exp(1j * 0.5) * op_a
    fidelity = abs(np.trace(op_a.conjugate().T @ op_b)) ** 2 / (op_a.shape[0] ** 2)
    return float(np.real_if_close(fidelity))


atexit.register(machine.finalize)
