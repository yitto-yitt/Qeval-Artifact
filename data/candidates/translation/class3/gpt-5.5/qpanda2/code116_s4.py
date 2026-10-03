# EVAL_META: task_id=116, framework=qpanda2, class=3
import atexit
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(16)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    if n > len(_qubits):
        raise ValueError("Pauli string is longer than the globally allocated qubit register.")

    circ = QCircuit()
    active = []

    for pos, pauli in enumerate(pauli_string):
        if pauli not in ("I", "X", "Y", "Z"):
            raise ValueError("Invalid Pauli character.")
        if pauli != "I":
            qidx = n - 1 - pos
            active.append((qidx, pauli))

    if not active:
        if n > 0:
            phase_matrix = (np.exp(-1j * time) * np.eye(2, dtype=complex)).tolist()
            try:
                circ.insert(QOracle([_qubits[0]], phase_matrix))
            except Exception:
                try:
                    circ.insert(matrix_decompose([_qubits[0]], phase_matrix))
                except Exception:
                    pass
        return circ

    for qidx, pauli in active:
        if pauli == "X":
            circ.insert(H(_qubits[qidx]))
        elif pauli == "Y":
            circ.insert(RZ(_qubits[qidx], -np.pi / 2))
            circ.insert(H(_qubits[qidx]))

    target = active[-1][0]
    for qidx, _ in active[:-1]:
        circ.insert(CNOT(_qubits[qidx], _qubits[target]))

    circ.insert(RZ(_qubits[target], 2 * time))

    for qidx, _ in reversed(active[:-1]):
        circ.insert(CNOT(_qubits[qidx], _qubits[target]))

    for qidx, pauli in reversed(active):
        if pauli == "X":
            circ.insert(H(_qubits[qidx]))
        elif pauli == "Y":
            circ.insert(H(_qubits[qidx]))
            circ.insert(RZ(_qubits[qidx], np.pi / 2))

    return circ

atexit.register(machine.finalize)
