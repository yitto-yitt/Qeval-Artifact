# EVAL_META: task_id=125, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def circ_to_gate(circ):
    program = pq.QProg()
    program << circ

    used_qubits = pq.QVec()
    program.get_used_qubits(used_qubits)
    ordered_qubits = sorted(
        used_qubits, key=lambda qubit: qubit.get_phy_addr()
    )

    matrix = pq.get_matrix(program)
    return pq.QOracle(ordered_qubits, matrix)


atexit.register(machine.finalize)
