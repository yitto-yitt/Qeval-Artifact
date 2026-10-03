# EVAL_META: task_id=112, framework=qpanda2, class=3
import math
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(128)
atexit.register(machine.finalize)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    if n > len(qubits):
        raise ValueError("Not enough globally allocated qubits for the requested circuit.")

    rep_count = int(reps)
    if rep_count <= 0:
        raise ValueError("reps must be a positive integer")

    prog = QProg()

    for pauli_string, time in zip(pauli_strings, times):
        pauli_string = str(pauli_string).upper()
        step_time = time / rep_count

        for _ in range(rep_count):
            active = []

            for pos, p in enumerate(pauli_string):
                qidx = n - 1 - pos
                qb = qubits[qidx]

                if p == "X":
                    prog.insert(H(qb))
                    active.append(qidx)
                elif p == "Y":
                    prog.insert(RZ(qb, -math.pi / 2))
                    prog.insert(H(qb))
                    active.append(qidx)
                elif p == "Z":
                    active.append(qidx)
                elif p == "I":
                    continue
                else:
                    raise ValueError("Invalid Pauli character: " + p)

            if len(active) == 1:
                prog.insert(RZ(qubits[active[0]], 2 * step_time))
            elif len(active) > 1:
                target = active[-1]
                for ctrl in active[:-1]:
                    prog.insert(CNOT(qubits[ctrl], qubits[target]))
                prog.insert(RZ(qubits[target], 2 * step_time))
                for ctrl in reversed(active[:-1]):
                    prog.insert(CNOT(qubits[ctrl], qubits[target]))

            for pos in range(len(pauli_string) - 1, -1, -1):
                p = pauli_string[pos]
                qidx = n - 1 - pos
                qb = qubits[qidx]

                if p == "X":
                    prog.insert(H(qb))
                elif p == "Y":
                    prog.insert(H(qb))
                    prog.insert(RZ(qb, math.pi / 2))

    return prog
