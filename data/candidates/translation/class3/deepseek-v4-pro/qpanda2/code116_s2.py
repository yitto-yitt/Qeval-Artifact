# EVAL_META: task_id=116, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

MAX_QUBITS = 20
qvm = CPUQVM()
qvm.initQVM()
q = qvm.qAlloc_many(MAX_QUBITS)

def synthesize_evolution_gate(pauli_string, time):
    pauli_str = pauli_string.upper()
    n = len(pauli_str)

    if n > MAX_QUBITS:
        raise ValueError("Pauli string too long for allocated qubit pool")

    circuit = QCircuit()
    non_id_qubits = []

    # Basis-change non-identity Paulis to Z
    for idx, ch in enumerate(pauli_str):
        if ch == 'I':
            continue
        if ch == 'X':
            circuit << H(q[idx])
        elif ch == 'Y':
            circuit << RX(q[idx], np.pi / 2.0)
        elif ch != 'Z':
            raise ValueError("Invalid Pauli character")
        non_id_qubits.append(idx)

    if not non_id_qubits:
        return circuit

    # CNOT staircase to encode the multi-Z interaction
    for i in range(len(non_id_qubits) - 1):
        circuit << CNOT(q[non_id_qubits[i]], q[non_id_qubits[i + 1]])

    # Rotation e^{-i * time * Z} on the last non-identity qubit
    circuit << RZ(q[non_id_qubits[-1]], 2.0 * time)

    # Uncompute the CNOT staircase
    for i in range(len(non_id_qubits) - 2, -1, -1):
        circuit << CNOT(q[non_id_qubits[i]], q[non_id_qubits[i + 1]])

    # Uncompute basis changes
    for idx in reversed(non_id_qubits):
        ch = pauli_str[idx]
        if ch == 'X':
            circuit << H(q[idx])
        elif ch == 'Y':
            circuit << RX(q[idx], -np.pi / 2.0)

    return circuit

if __name__ == "__main__":
    qvm.finalize()
