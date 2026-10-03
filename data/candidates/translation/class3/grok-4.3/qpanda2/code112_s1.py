# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *
from math import pi
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)
def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qs = qubits[:n]
    prog = create_empty_qprog()
    for _ in range(reps):
        for pstr, t in zip(pauli_strings, times):
            append_pauli_evolution(prog, qs, pstr, t / reps)
    return prog
def append_pauli_evolution(prog, qs, pauli, time):
    angle = 2 * time
    pauli_list = list(pauli)
    active_indices = [i for i, p in enumerate(pauli_list) if p != 'I']
    if not active_indices:
        return
    for i, p in enumerate(pauli_list):
        if p == 'X':
            prog << H(qs[i])
        elif p == 'Y':
            prog << RX(qs[i], pi / 2)
    target = active_indices[-1]
    for idx in active_indices[:-1]:
        prog << CNOT(qs[idx], qs[target])
    prog << RZ(qs[target], angle)
    for idx in reversed(active_indices[:-1]):
        prog << CNOT(qs[idx], qs[target])
    for i, p in enumerate(pauli_list):
        if p == 'X':
            prog << H(qs[i])
        elif p == 'Y':
            prog << RX(qs[i], -pi / 2)
machine.finalize()
