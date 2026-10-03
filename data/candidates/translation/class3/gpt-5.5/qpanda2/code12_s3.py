# EVAL_META: task_id=12, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def get_unitary():
    try:
        prog = pq.QProg()
        prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
        unitary = np.array(pq.get_unitary(prog), dtype=complex)

        probe_prog = pq.QProg()
        probe_prog << pq.H(qubits[0]) << pq.I(qubits[1])
        probe = np.array(pq.get_unitary(probe_prog), dtype=complex)

        if probe.shape == (4, 4) and abs(probe[0, 2]) > abs(probe[0, 1]):
            perm = [0, 2, 1, 3]
            unitary = unitary[np.ix_(perm, perm)]

        return unitary
    finally:
        machine.finalize()
