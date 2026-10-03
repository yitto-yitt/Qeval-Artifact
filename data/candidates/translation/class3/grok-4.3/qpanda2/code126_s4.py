# EVAL_META: task_id=126, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
def calculate_phase_difference_fidelity():
    def get_unitary():
        dim = 2
        unitary = np.zeros((dim, dim), dtype=complex)
        for i in range(dim):
            prog = pq.QProg()
            if i == 1:
                prog << pq.X(qubits[0])
            prog << pq.H(qubits[0])
            machine.directly_run(prog)
            unitary[:, i] = machine.get_qstate()
        return unitary
    op_a = get_unitary()
    op_b = np.exp(1j * 0.5) * op_a
    d = op_a.shape[0]
    trace_val = np.trace(np.dot(np.conj(op_a).T, op_b))
    fidelity = np.abs(trace_val)**2 / d**2
    return fidelity
machine.finalize()
