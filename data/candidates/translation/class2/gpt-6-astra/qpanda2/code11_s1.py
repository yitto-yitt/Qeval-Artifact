# EVAL_META: task_id=11, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq


def get_statevector(circuit):
    program = pq.QProg()
    program << circuit

    used_qubits = pq.QVec()
    program.get_used_qubits(used_qubits)
    num_qubits = max(
        (qubit.get_phy_addr() for qubit in used_qubits),
        default=-1,
    ) + 1

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        machine.qAlloc_many(num_qubits)
        machine.directly_run(program)
        return np.array(machine.get_qstate(), dtype=np.complex128)
    finally:
        machine.finalize()
