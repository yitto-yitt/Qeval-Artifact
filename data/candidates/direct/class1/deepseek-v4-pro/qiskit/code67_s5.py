# EVAL_META: task_id=67, framework=qiskit, class=1
from qiskit import QuantumCircuit
from math import pi


def chsh_circuit(alice, bob):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)

    if alice == 1:
        qc.h(0)

    if bob == 0:
        qc.ry(-pi / 4, 1)
    else:
        qc.ry(pi / 4, 1)

    qc.measure([0, 1], [0, 1])
    return qc
