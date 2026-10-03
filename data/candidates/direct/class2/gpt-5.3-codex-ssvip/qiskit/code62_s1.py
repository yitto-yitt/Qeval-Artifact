# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit


def bb84_senders_circuit(state, basis):
    n = len(state)
    if len(basis) != n:
        raise ValueError("state and basis must have the same length")

    qc = QuantumCircuit(n, n)

    for i, (s, b) in enumerate(zip(state, basis)):
        if s in (1, "1"):
            qc.x(i)
        elif s in (0, "0"):
            pass
        else:
            raise ValueError("state values must be binary (0/1)")

        if b in (1, "1"):
            qc.h(i)
        elif b in (0, "0"):
            pass
        else:
            raise ValueError("basis values must be binary (0/1)")

    qc.measure(range(n), range(n))
    return qc
