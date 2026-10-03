# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit


def bb84_senders_circuit(state, basis):
    n = len(state)
    if len(basis) != n:
        raise ValueError("state and basis must have the same length")

    qc = QuantumCircuit(n, n)

    for i, (s, b) in enumerate(zip(state, basis)):
        if s not in (0, 1):
            raise ValueError("state entries must be 0 or 1")
        if b not in (0, 1):
            raise ValueError("basis entries must be 0 or 1")

        if s == 1:
            qc.x(i)
        if b == 1:
            qc.h(i)

    for i, b in enumerate(basis):
        if b == 1:
            qc.h(i)
        qc.measure(i, i)

    return qc
