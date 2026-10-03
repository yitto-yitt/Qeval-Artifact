# EVAL_META: task_id=116, framework=qpanda2, class=3
import math
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
qubit_count = 1


def synthesize_evolution_gate(pauli_string, time):
    global qubits, qubit_count

    n = len(pauli_string)
    if qubit_count < n:
        qubits = machine.qAlloc_many(n)
        qubit_count = n

    circuit = QCircuit()
    inds = [i for i, p in enumerate(pauli_string) if p != 'I']

    # Basis change: map X/Y to Z
    for idx in inds:
        p = pauli_string[idx]
        if p == 'X':
            circuit << H(qubits[idx])
        elif p == 'Y':
            circuit << RX(qubits[idx], -math.pi / 2)

    # CNOT cascade to compute parity on the last non-I qubit
    if inds:
        for ctrl, target in zip(inds[:-1], inds[1:]):
            circuit << CNOT(qubits[ctrl], qubits[target])

        circuit << RZ(qubits[inds[-1]], 2 * time)

        for ctrl, target in reversed(list(zip(inds[:-1], inds[1:]))):
            circuit << CNOT(qubits[ctrl], qubits[target])

    # Undo basis change
    for idx in inds:
        p = pauli_string[idx]
        if p == 'X':
            circuit << H(qubits[idx])
        elif p == 'Y':
            circuit << RX(qubits[idx], math.pi / 2)

    return circuit


atexit.register(machine.finalize)
