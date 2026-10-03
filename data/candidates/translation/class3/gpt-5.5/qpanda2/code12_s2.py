# EVAL_META: task_id=12, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)
atexit.register(machine.finalize)


def get_unitary():
    def as_matrix(obj, dim):
        mat = np.asarray(obj, dtype=complex)
        if mat.ndim == 1:
            mat = mat.reshape((dim, dim))
        return mat

    def full_x_matrix(qubit_index):
        circ = pq.QCircuit()
        circ << pq.CNOT(q[0], q[1]) << pq.CNOT(q[0], q[1]) << pq.X(q[qubit_index])
        return as_matrix(pq.get_matrix(circ), 4)

    positions = []
    for i in range(2):
        xmat = full_x_matrix(i)
        row = int(np.argmax(np.abs(xmat[:, 0])))
        positions.append(0 if row == 1 else 1)

    circ = pq.QCircuit()
    circ << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    mat_py = as_matrix(pq.get_matrix(circ), 4)

    perm = np.zeros((4, 4), dtype=complex)
    for b0 in range(2):
        for b1 in range(2):
            qiskit_index = b0 + 2 * b1
            py_index = (b0 << positions[0]) + (b1 << positions[1])
            perm[qiskit_index, py_index] = 1.0

    return perm @ mat_py @ perm.T
