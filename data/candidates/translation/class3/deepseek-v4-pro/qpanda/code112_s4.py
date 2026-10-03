# EVAL_META: task_id=112, framework=qpanda, class=3
import math
from pyqpanda3.core import QuantumCircuit


def _append_pauli_evolution(qc, pauli_string, time):
    target_indices = [i for i, p in enumerate(pauli_string) if p != 'I']
    if not target_indices:
        return

    # Rotate to the Z basis.
    for i in target_indices:
        p = pauli_string[i]
        if p == 'X':
            qc.h(i)
        elif p == 'Y':
            qc.rx(i, math.pi / 2)

    last = target_indices[-1]

    # Parity ladder.
    for i in target_indices[:-1]:
        qc.cnot(i, last)

    qc.rz(last, 2.0 * time)

    # Uncompute parity ladder.
    for i in reversed(target_indices[:-1]):
        qc.cnot(i, last)

    # Restore original basis.
    for i in reversed(target_indices):
        p = pauli_string[i]
        if p == 'X':
            qc.h(i)
        elif p == 'Y':
            qc.rx(i, -math.pi / 2)


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    qc = QuantumCircuit(n_qubits)

    for pauli_string, t in zip(pauli_strings, times):
        step_time = t / reps
        for _ in range(reps):
            _append_pauli_evolution(qc, pauli_string, step_time)

    return qc
