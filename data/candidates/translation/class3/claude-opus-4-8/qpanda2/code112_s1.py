# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)


def _append_pauli_evolution(prog, qs, pauli_string, time, reps):
    n = len(pauli_string)
    # qiskit Pauli string: leftmost char is highest qubit index
    # pauli_string[i] corresponds to qubit (n-1-i)
    dt = time / reps
    for _ in range(reps):
        active = []
        for i, p in enumerate(pauli_string):
            q = n - 1 - i
            if p != 'I':
                active.append((q, p))
        if not active:
            continue
        # basis change
        for q, p in active:
            if p == 'X':
                prog << H(qs[q])
            elif p == 'Y':
                prog << RX(qs[q], np.pi / 2)
        # CNOT ladder
        idxs = [q for q, _ in active]
        for k in range(len(idxs) - 1):
            prog << CNOT(qs[idxs[k]], qs[idxs[k + 1]])
        # rotation on last qubit
        prog << RZ(qs[idxs[-1]], 2 * dt)
        # undo CNOT ladder
        for k in range(len(idxs) - 2, -1, -1):
            prog << CNOT(qs[idxs[k]], qs[idxs[k + 1]])
        # undo basis change
        for q, p in active:
            if p == 'X':
                prog << H(qs[q])
            elif p == 'Y':
                prog << RX(qs[q], -np.pi / 2)


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qs = [qubits[i] for i in range(n)]
    prog = QProg()
    for pauli_string, time in zip(pauli_strings, times):
        _append_pauli_evolution(prog, qs, pauli_string, time, reps)
    return prog
