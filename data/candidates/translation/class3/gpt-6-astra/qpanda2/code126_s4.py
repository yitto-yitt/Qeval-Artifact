# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QProg, H, CNOT, RZ, U1

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def calculate_phase_difference_fidelity():
    try:
        program_a = QProg()
        program_a << H(qubits[0]) << CNOT(qubits[0], qubits[1])
        program_a << H(qubits[1])

        machine.directly_run(program_a)
        choi_a = np.array(machine.get_qstate(), dtype=complex)

        program_b = QProg()
        program_b << H(qubits[0]) << CNOT(qubits[0], qubits[1])
        program_b << H(qubits[1])
        # RZ(-1) followed by U1(1) implements exp(0.5j) * I.
        program_b << RZ(qubits[1], -1.0) << U1(qubits[1], 1.0)

        machine.directly_run(program_b)
        choi_b = np.array(machine.get_qstate(), dtype=complex)

        return float(np.abs(np.vdot(choi_a, choi_b)) ** 2)
    finally:
        machine.finalize()
