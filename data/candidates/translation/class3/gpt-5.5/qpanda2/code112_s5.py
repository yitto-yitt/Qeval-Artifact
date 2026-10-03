# EVAL_META: task_id=112, framework=qpanda2, class=3
import math
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(32)
atexit.register(machine.finalize)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    prog = QProg()

    for pauli_string, time in zip(pauli_strings, times):
        for _ in range(reps):
            active = []
            for i in range(n):
                p = pauli_string[n - 1 - i]
                if p != "I":
                    active.append(i)
                    if p == "X":
                        prog << H(q[i])
                    elif p == "Y":
                        prog << RX(q[i], math.pi / 2)

            if active:
                target = active[-1]
                for control in active[:-1]:
                    prog << CNOT(q[control], q[target])

                prog << RZ(q[target], 2 * time / reps)

                for control in reversed(active[:-1]):
                    prog << CNOT(q[control], q[target])

                for i in reversed(active):
                    p = pauli_string[n - 1 - i]
                    if p == "X":
                        prog << H(q[i])
                    elif p == "Y":
                        prog << RX(q[i], -math.pi / 2)

    return prog
