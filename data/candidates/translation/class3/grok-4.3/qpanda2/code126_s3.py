# EVAL_META: task_id=126, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
def calculate_phase_difference_fidelity():
    machine.set_qstate([1, 0])
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    machine.directly_run(prog)
    state0 = machine.get_qstate()
    machine.set_qstate([0, 1])
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    machine.directly_run(prog)
    state1 = machine.get_qstate()
    matrix_a = np.array([state0, state1]).T
    phase = np.exp(1j * 0.5)
    matrix_b = phase * matrix_a
    d = 2
    UdagV = matrix_a.conj().T @ matrix_b
    trace = np.trace(UdagV)
    fidelity = np.abs(trace)**2 / d**2
    return fidelity
machine.finalize()
