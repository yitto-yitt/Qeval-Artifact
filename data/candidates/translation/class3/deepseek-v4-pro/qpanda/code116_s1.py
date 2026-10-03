# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3 import QCircuit, H, CNOT, RZ, RX
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    circuit = QCircuit()

    # If all identity, return circuit that acts as identity on n qubits
    if all(p == 'I' for p in pauli_string):
        for i in range(n):
            circuit << H(i) << H(i)  # identity using H^2
        return circuit

    # Find first non-identity qubit as the target for the CNOT network
    target = None
    for i, p in enumerate(pauli_string):
        if p != 'I':
            target = i
            break

    # Apply single-qubit basis changes to map Paulis to Z
    basis_changes = []
    for i, p in enumerate(pauli_string):
        if p == 'X':
            circuit << H(i)
            basis_changes.append(('X', i))
        elif p == 'Y':
            circuit << RX(i, np.pi/2)
            basis_changes.append(('Y', i))
        # Z and I need no basis change

    # Build CNOT ladder to collect parity on the target qubit
    cnots = []
    for i, p in enumerate(pauli_string):
        if p != 'I' and i != target:
            circuit << CNOT(i, target)
            cnots.append((i, target))

    # Apply the phase rotation on the target qubit
    circuit << RZ(target, 2 * time)

    # Reverse the CNOT ladder
    for i, tgt in reversed(cnots):
        circuit << CNOT(i, tgt)

    # Reverse the basis changes
    for op, i in basis_changes:
        if op == 'X':
            circuit << H(i)        # H is self-inverse
        elif op == 'Y':
            circuit << RX(i, -np.pi/2)

    return circuit
