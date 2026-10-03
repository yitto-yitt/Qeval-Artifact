# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit


def bb84_senders_circuit(state, basis):
    state_bits = [int(x) for x in state]
    basis_bits = [int(x) for x in basis]

    n = len(state_bits)
    qc = QuantumCircuit(n)

    for i in range(n):
        if state_bits[i] == 1:
            qc.x(i)
        if basis_bits[i] == 1:
            qc.h(i)

    return qc
