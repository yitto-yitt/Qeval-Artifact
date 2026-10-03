# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import *

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n_qubits)

    prog = QProg()

    for pauli_string, t in zip(pauli_strings, times):
        for _ in range(reps):
            # First-order Lie-Trotter step for each Pauli term
            active = [i for i, p in enumerate(pauli_string) if p != 'I']
            if not active:
                continue

            # Basis change to Z for X/Y terms
            for i in active:
                p = pauli_string[i]
                if p == 'X':
                    prog << H(q[i])
                elif p == 'Y':
                    prog << RX(q[i], 1.5707963267948966)

            # Parity entangling chain
            for i in range(len(active) - 1):
                prog << CNOT(q[active[i]], q[active[i + 1]])

            # RZ rotation on last active qubit
            angle = 2.0 * float(t) / float(reps)
            prog << RZ(q[active[-1]], angle)

            # Uncompute parity chain
            for i in range(len(active) - 2, -1, -1):
                prog << CNOT(q[active[i]], q[active[i + 1]])

            # Undo basis change
            for i in active:
                p = pauli_string[i]
                if p == 'X':
                    prog << H(q[i])
                elif p == 'Y':
                    prog << RX(q[i], -1.5707963267948966)

    return prog
