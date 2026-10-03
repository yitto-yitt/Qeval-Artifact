# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(10)
def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qlist = qubits[:n]
    prog = QProg()
    for pauli_str, t in zip(pauli_strings, times):
        delta = t / reps
        for _ in range(reps):
            for i, p in enumerate(pauli_str):
                if p == 'X':
                    prog.insert(H(qlist[i]))
                elif p == 'Y':
                    prog.insert(Sdag(qlist[i]))
                    prog.insert(H(qlist[i]))
            for i in range(n-1):
                prog.insert(CNOT(qlist[i], qlist[n-1]))
            prog.insert(RZ(qlist[n-1], 2 * delta))
            for i in reversed(range(n-1)):
                prog.insert(CNOT(qlist[i], qlist[n-1]))
            for i, p in enumerate(pauli_str):
                if p == 'X':
                    prog.insert(H(qlist[i]))
                elif p == 'Y':
                    prog.insert(H(qlist[i]))
                    prog.insert(S(qlist[i]))
    return prog
machine.finalize()
