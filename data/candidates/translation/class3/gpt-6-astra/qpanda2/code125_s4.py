# EVAL_META: task_id=125, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def circ_to_gate(circ):
    prog = pq.QProg()
    prog << circ

    used_qubits = pq.QVec()
    try:
        pq.get_all_used_qubits(prog, used_qubits)
    except TypeError:
        used_qubits = pq.get_all_used_qubits(prog)

    ordered_qubits = sorted(used_qubits, key=lambda q: q.get_phy_addr())
    matrix = np.asarray(pq.get_matrix(prog), dtype=complex)
    return pq.QOracle(ordered_qubits, matrix.reshape(-1).tolist())


machine.finalize()
