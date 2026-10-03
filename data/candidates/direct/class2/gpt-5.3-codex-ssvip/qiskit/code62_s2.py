# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit


def bb84_senders_circuit(state, basis):
    if len(state) != len(basis):
        raise ValueError("state and basis must have the same length")

    n = len(state)
    qc = QuantumCircuit(n, n)

    for i, (s, b) in enumerate(zip(state, basis)):
        if s not in (0, 1):
            raise ValueError("state elements must be 0 or 1")
        if b not in (0, 1):
            raise ValueError("basis elements must be 0 or 1")

        if b == 0:
            if s == 1:
                qc.x(i)
        else:
            if s == 0:
                qc.h(i)
            else:
                qc.x(i)
                qc.h(i)

        if b == 1:
            qc.h(i)
        qc.measure(i, i)

    return qc
