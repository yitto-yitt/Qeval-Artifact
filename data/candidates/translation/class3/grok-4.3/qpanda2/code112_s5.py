# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)
def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    qlist = qubits[:n_qubits]
    prog = QProg()
    for pauli_string, time in zip(pauli_strings, times):
        delta = time / reps
        for _ in range(reps):
            active = [i for i, p in enumerate(pauli_string) if p != 'I']
            if not active:
                continue
            for i, p in enumerate(pauli_string):
                if p == 'X':
                    prog << H(qlist[i])
                elif p == 'Y':
                    prog << RX(qlist[i], -np.pi / 2)
            for j in range(len(active) - 1):
                prog << CNOT(qlist[active[j]], qlist[active[j + 1]])
            prog << RZ(qlist[active[-1]], 2 * delta)
            for j in range(len(active) - 2, -1, -1):
                prog << CNOT(qlist[active[j]], qlist[active[j + 1]])
            for i, p in enumerate(pauli_string):
                if p == 'X':
                    prog << H(qlist[i])
                elif p == 'Y':
                    prog << RX(qlist[i], np.pi / 2)
    return prog
machine.finalize()
