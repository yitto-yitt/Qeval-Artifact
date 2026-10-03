# EVAL_META: task_id=125, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def circ_to_gate(circ):
    prog = pq.QProg()
    prog << circ
    used_qubits = sorted(
        pq.get_all_used_qubits(prog),
        key=lambda qubit: qubit.get_phy_addr(),
    )
    matrix = np.asarray(pq.get_matrix(prog), dtype=complex)
    return pq.QOracle(used_qubits, matrix.reshape(-1).tolist())


machine.finalize()
