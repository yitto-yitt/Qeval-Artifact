# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import *

def create_product_formula_circuit(pauli_strings, times, order, reps):
    if not pauli_strings:
        machine = CPUQVM()
        machine.init_qvm()
        return machine, QProg(), []

    n_qubits = len(pauli_strings[0])
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n_qubits)

    prog = QProg()

    for pauli_string, t in zip(pauli_strings, times):
        for _ in range(reps):
            for i, p in enumerate(pauli_string):
                if p == 'I':
                    continue
                angle = 2.0 * float(t) / float(reps)
                if p == 'X':
                    prog << RX(q[i], angle)
                elif p == 'Y':
                    prog << RY(q[i], angle)
                elif p == 'Z':
                    prog << RZ(q[i], angle)

    return machine, prog, q
