# EVAL_META: task_id=116, framework=qpanda, class=3
import math
from pyqpanda3.core import CPUQVM, QCircuit, H, CNOT, RZ

_QVM = None


def _get_qvm():
    global _QVM
    if _QVM is None:
        _QVM = CPUQVM()
        _QVM.init_qvm()
    return _QVM


def synthesize_evolution_gate(pauli_string, time):
    pauli_string = pauli_string.strip().upper()
    n = len(pauli_string)
    if n == 0:
        return QCircuit()

    qvm = _get_qvm()
    qubits = qvm.qAlloc_many(n)

    circuit = QCircuit()

    # Ensure all I qubits are present in the circuit.
    for i, p in enumerate(pauli_string):
        if p == 'I':
            circuit << RZ(qubits[i], 0.0)

    positions = [i for i, p in enumerate(pauli_string) if p != 'I']

    # Basis changes for X and Y so each non-I Pauli becomes Z.
    for i in positions:
        p = pauli_string[i]
        if p == 'X':
            circuit << H(qubits[i])
        elif p == 'Y':
            circuit << RZ(qubits[i], -math.pi / 2.0)
            circuit << H(qubits[i])

    # Parity ladder over the non-I qubits.
    for j in range(len(positions) - 1):
        circuit << CNOT(qubits[positions[j]], qubits[positions[j + 1]])

    if positions:
        circuit << RZ(qubits[positions[-1]], 2.0 * time)

    # Inverse parity ladder.
    for j in reversed(range(len(positions) - 1)):
        circuit << CNOT(qubits[positions[j]], qubits[positions[j + 1]])

    # Undo basis transformations.
    for i in reversed(positions):
        p = pauli_string[i]
        if p == 'X':
            circuit << H(qubits[i])
        elif p == 'Y':
            circuit << H(qubits[i])
            circuit << RZ(qubits[i], math.pi / 2.0)

    return circuit
