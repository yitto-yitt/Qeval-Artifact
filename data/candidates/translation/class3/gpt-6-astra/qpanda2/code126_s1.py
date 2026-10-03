# EVAL_META: task_id=126, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
atexit.register(lambda: machine.finalize())


def calculate_phase_difference_fidelity():
    columns = []
    for basis in range(2):
        program = pq.QProg()
        if basis:
            program << pq.X(qubits[0])
        program << pq.H(qubits[0])
        machine.directly_run(program)
        columns.append(np.asarray(machine.get_qstate(), dtype=complex))

    op_a = np.column_stack(columns)
    op_b = np.exp(1j * 0.5) * op_a
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b)) ** 2 / 4.0
    return float(fidelity)
