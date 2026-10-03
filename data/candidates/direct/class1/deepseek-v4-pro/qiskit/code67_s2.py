# EVAL_META: task_id=67, framework=qiskit, class=1

from math import pi

from qiskit import QuantumCircuit


def chsh_circuit(alice, bob):
    qc = QuantumCircuit(2, 2)

    # Create a shared Bell pair.
    qc.h(0)
    qc.cx(0, 1)

    # Alice's measurement choice:
    # 0 -> Z basis, 1 -> X basis.
    if alice == 1:
        qc.h(0)

    # Bob's measurement choice:
    # 0 -> (Z + X)/sqrt(2), 1 -> (Z - X)/sqrt(2).
    if bob == 0:
        qc.ry(-pi / 4, 1)
    else:
        qc.ry(pi / 4, 1)

    # Measure both qubits.
    qc.measure(0, 0)
    qc.measure(1, 1)

    return qc
