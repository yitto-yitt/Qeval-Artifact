# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import *

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0]) if pauli_strings else 0
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n)
    prog = QProg()

    for _ in range(max(1, reps)):
        for pauli_string, t in zip(pauli_strings, times):
            for i, p in enumerate(pauli_string):
                if p == 'X':
                    prog << RX(q[i], 2.0 * float(t))
                elif p == 'Y':
                    prog << RY(q[i], 2.0 * float(t))
                elif p == 'Z':
                    prog << RZ(q[i], 2.0 * float(t))
                else:
                    pass

    return prog
