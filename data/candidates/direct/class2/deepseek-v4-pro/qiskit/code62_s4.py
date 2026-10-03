# EVAL_META: task_id=62, framework=qiskit, class=2

from qiskit import QuantumCircuit


def bb84_senders_circuit(state, basis):
    if isinstance(state, (int, bool)):
        state = [int(state)]
    else:
        state = [int(bit) for bit in state]

    if isinstance(basis, (int, bool)):
        basis = [int(basis)]
    else:
        basis = [int(bit) for bit in basis]

    if len(state) != len(basis):
        raise ValueError("state and basis must have the same length")

    qc = QuantumCircuit(len(state))

    for qubit, (bit, base) in enumerate(zip(state, basis)):
        if bit:
            qc.x(qubit)
        if base:
            qc.h(qubit)

    return qc
