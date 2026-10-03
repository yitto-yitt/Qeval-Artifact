# EVAL_META: task_id=112, framework=qpanda, class=3
import math
from pyqpanda3.core import QuantumCircuit

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    qc = QuantumCircuit(num_qubits)

    for pauli_string, time in zip(pauli_strings, times):
        active_qubits = [q for q, p in enumerate(pauli_string) if p != 'I']

        if not active_qubits:
            continue

        # Map each non-I Pauli to Z.
        for q in active_qubits:
            p = pauli_string[q]
            if p == 'X':
                qc.h(q)
            elif p == 'Y':
                qc.rx(q, math.pi / 2)
            elif p == 'Z':
                pass
            else:
                raise ValueError(f"Unsupported Pauli character: {p}")

        # Apply e^{-i time * Z...Z} via a CNOT parity ladder.
        k = len(active_qubits)
        if k == 1:
            qc.rz(active_qubits[0], 2 * time)
        else:
            for i in range(k - 1):
                qc.cnot(active_qubits[i], active_qubits[i + 1])
            qc.rz(active_qubits[-1], 2 * time)
            for i in reversed(range(k - 1)):
                qc.cnot(active_qubits[i], active_qubits[i + 1])

        # Undo basis transformations.
        for q in reversed(active_qubits):
            p = pauli_string[q]
            if p == 'X':
                qc.h(q)
            elif p == 'Y':
                qc.rx(q, -math.pi / 2)
            elif p == 'Z':
                pass

    return qc
