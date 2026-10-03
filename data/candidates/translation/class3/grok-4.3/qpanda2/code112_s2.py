# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    qlist = qubits[:n_qubits]
    prog = QProg()
    for pauli_string, t in zip(pauli_strings, times):
        dt = t / reps if reps > 0 else t
        for _ in range(reps):
            for i, p in enumerate(pauli_string):
                if p == 'X':
                    prog << H(qlist[i])
                elif p == 'Y':
                    prog << RX(qlist[i], -np.pi / 2)
            active = [qlist[i] for i in range(n_qubits) if pauli_string[i] != 'I']
            if active:
                target = active[-1]
                for ctrl in active[:-1]:
                    prog << CNOT(ctrl, target)
                prog << RZ(target, 2 * dt)
                for ctrl in reversed(active[:-1]):
                    prog << CNOT(ctrl, target)
            for i, p in enumerate(pauli_string):
                if p == 'X':
                    prog << H(qlist[i])
                elif p == 'Y':
                    prog << RX(qlist[i], np.pi / 2)
    return prog

machine.finalize()
