# EVAL_META: task_id=116, framework=qpanda2, class=3
import numpy as np
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.initQVM()
atexit.register(machine.finalize)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    if n == 0:
        return QCircuit()

    q = machine.qAlloc_many(n)
    circ = QCircuit()

    # Diagonalize X/Y to Z basis
    for i, p in enumerate(pauli_string):
        if p == 'X':
            circ << H(q[i])
        elif p == 'Y':
            circ << RZ(q[i], -np.pi / 2)
            circ << H(q[i])

    nonI = [i for i, p in enumerate(pauli_string) if p != 'I']

    if len(nonI) == 1:
        circ << RZ(q[nonI[0]], 2 * time)
    elif len(nonI) > 1:
        target = nonI[-1]
        for i in nonI[:-1]:
            circ << CNOT(q[i], q[target])
        circ << RZ(q[target], 2 * time)
        for i in reversed(nonI[:-1]):
            circ << CNOT(q[i], q[target])

    # Undo basis changes
    for i in reversed(range(n)):
        p = pauli_string[i]
        if p == 'X':
            circ << H(q[i])
        elif p == 'Y':
            circ << H(q[i])
            circ << RZ(q[i], np.pi / 2)

    return circ
