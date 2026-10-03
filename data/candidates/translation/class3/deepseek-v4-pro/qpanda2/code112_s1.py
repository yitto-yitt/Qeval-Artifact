# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(20)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    circuit = QCircuit()

    for pauli_str, t in zip(pauli_strings, times):
        tau = t / reps
        for _ in range(reps):
            pauli_str = pauli_str.upper()
            non_idxs = [i for i, ch in enumerate(pauli_str) if ch != 'I']

            if not non_idxs:
                continue

            for i in non_idxs:
                ch = pauli_str[i]
                if ch == 'X':
                    circuit << H(q[i])
                elif ch == 'Y':
                    circuit << RZ(q[i], -np.pi / 2)
                    circuit << H(q[i])

            if len(non_idxs) == 1:
                circuit << RZ(q[non_idxs[0]], 2 * tau)
            else:
                for k in range(len(non_idxs) - 1):
                    circuit << CNOT(q[non_idxs[k]], q[non_idxs[k + 1]])
                circuit << RZ(q[non_idxs[-1]], 2 * tau)
                for k in reversed(range(len(non_idxs) - 1)):
                    circuit << CNOT(q[non_idxs[k]], q[non_idxs[k + 1]])

            for i in reversed(non_idxs):
                ch = pauli_str[i]
                if ch == 'X':
                    circuit << H(q[i])
                elif ch == 'Y':
                    circuit << H(q[i])
                    circuit << RZ(q[i], np.pi / 2)

    return circuit

machine.finalize()
