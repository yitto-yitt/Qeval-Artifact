# EVAL_META: task_id=117, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq

def decompose_unitary(unitary):
    mat = np.asarray(unitary, dtype=complex)

    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    qubits = machine.qAlloc_many(2)

    if not hasattr(decompose_unitary, "_machines"):
        decompose_unitary._machines = []
    decompose_unitary._machines.append(machine)

    f = pq.matrix_decompose
    for args in (
        (qubits, mat),
        (qubits, mat.tolist()),
        (mat, qubits),
        (mat.tolist(), qubits),
        (machine, qubits, mat),
        (machine, qubits, mat.tolist()),
    ):
        try:
            return f(*args)
        except TypeError:
            pass

    return f(qubits, mat)
