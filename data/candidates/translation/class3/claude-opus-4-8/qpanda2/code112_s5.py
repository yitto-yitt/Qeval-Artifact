# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)


def _pauli_evolution(qlist, pauli_string, time, reps):
    prog = QProg()
    n = len(pauli_string)
    dt = time / reps
    for _ in range(reps):
        active = [(i, p) for i, p in enumerate(pauli_string) if p != 'I']
        if not active:
            continue
        # basis change
        for i, p in active:
            q = qlist[n - 1 - i]
            if p == 'X':
                prog << H(q)
            elif p == 'Y':
                prog << RX(q, np.pi / 2)
        idxs = [n - 1 - i for i, p in active]
        for k in range(len(idxs) - 1):
            prog << CNOT(qlist[idxs[k]], qlist[idxs[k + 1]])
        prog << RZ(qlist[idxs[-1]], 2 * dt)
        for k in range(len(idxs) - 2, -1, -1):
            prog << CNOT(qlist[idxs[k]], qlist[idxs[k + 1]])
        for i, p in active:
            q = qlist[n - 1 - i]
            if p == 'X':
                prog << H(q)
            elif p == 'Y':
                prog << RX(q, -np.pi / 2)
    return prog


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qlist = [qubits[i] for i in range(n)]
    prog = QProg()
    for pauli_string, time in zip(pauli_strings, times):
        prog << _pauli_evolution(qlist, pauli_string, time, reps)
    return prog
