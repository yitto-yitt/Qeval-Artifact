# EVAL_META: task_id=125, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(29)


def circ_to_gate(circ):
    prog = pq.QProg()
    prog << circ
    matrix = np.asarray(pq.get_matrix(prog), dtype=np.complex128).reshape(-1)
    num_qubits = (int(matrix.size).bit_length() - 1) // 2
    return pq.QOracle(qubits[:num_qubits], matrix.tolist())


atexit.register(machine.finalize)
