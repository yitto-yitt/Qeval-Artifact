# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
import atexit

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(100)
atexit.register(machine.finalize)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    q = qubits[:n]
    circuit = QCircuit()
    for pauli_str, t in zip(pauli_strings, times):
        support = [i for i, c in enumerate(pauli_str) if c != 'I']
        if not support:
            continue
        first = support[0]
        for _ in range(reps):
            dt = t / reps
            # basis change
            for i in support:
                c = pauli_str[i]
                if c == 'X':
                    circuit << H(q[i])
                elif c == 'Y':
                    circuit << Sdag(q[i])
                    circuit << H(q[i])
            # CNOT chain
            for i in support[1:]:
                circuit << CNOT(q[i], q[first])
            # RZ
            circuit << RZ(q[first], 2 * dt)
            # reverse CNOT
            for i in reversed(support[1:]):
                circuit << CNOT(q[i], q[first])
            # reverse basis change
            for i in support:
                c = pauli_str[i]
                if c == 'X':
                    circuit << H(q[i])
                elif c == 'Y':
                    circuit << H(q[i])
                    circuit << S(q[i])
    return circuit
