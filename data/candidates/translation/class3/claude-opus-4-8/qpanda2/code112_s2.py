# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, QProg
from pyqpanda import H, RX, RZ, CNOT

machine = CPUQVM()
machine.init_qvm()


def _pauli_evolution(qubits, pauli_string, time, reps):
    circ = QCircuit()
    n = len(pauli_string)
    # LieTrotter for a single Pauli term: repeat exp(-i * (time/reps) * P) reps times
    dt = time / reps
    # indices of non-identity paulis (Qiskit Pauli string is little-endian:
    # rightmost char is qubit 0)
    for _ in range(reps):
        active = []
        basis = QCircuit()
        basis_inv = QCircuit()
        for i, ch in enumerate(pauli_string):
            q = n - 1 - i  # qubit index for this character
            if ch == 'I':
                continue
            active.append(q)
            if ch == 'X':
                basis << H(qubits[q])
                basis_inv << H(qubits[q])
            elif ch == 'Y':
                basis << RX(qubits[q], 1.5707963267948966)
                basis_inv << RX(qubits[q], -1.5707963267948966)
        if not active:
            continue
        active.sort()
        circ << basis
        for k in range(len(active) - 1):
            circ << CNOT(qubits[active[k]], qubits[active[k + 1]])
        circ << RZ(qubits[active[-1]], 2.0 * dt)
        for k in range(len(active) - 1, 0, -1):
            circ << CNOT(qubits[active[k - 1]], qubits[active[k]])
        circ << basis_inv
    return circ


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = machine.qAlloc_many(n)
    prog = QProg()
    for pauli_string, time in zip(pauli_strings, times):
        prog << _pauli_evolution(qubits, pauli_string, time, reps)
    return prog
