# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit


def bb84_senders_circuit(state, basis):
    if len(state) != len(basis):
        raise ValueError("state and basis must have the same length")

    n = len(state)
    qc = QuantumCircuit(n, n)

    for i, (s, b) in enumerate(zip(state, basis)):
        s_bit = int(s)
        b_bit = int(b)

        if b_bit == 0:
            if s_bit == 1:
                qc.x(i)
        elif b_bit == 1:
            if s_bit == 1:
                qc.x(i)
            qc.h(i)
        else:
            raise ValueError("basis entries must be 0 or 1")

    for i, b in enumerate(basis):
        b_bit = int(b)
        if b_bit == 1:
            qc.h(i)
        elif b_bit != 0:
            raise ValueError("basis entries must be 0 or 1")
        qc.measure(i, i)

    return qc
