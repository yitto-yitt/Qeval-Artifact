# EVAL_META: task_id=67, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit

def chsh_circuit(alice, bob):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)

    if alice == 1:
        qc.h(0)

    if bob == 0:
        qc.ry(-np.pi / 4, 1)
    else:
        qc.ry(np.pi / 4, 1)

    qc.measure([0, 1], [0, 1])
    return qc
