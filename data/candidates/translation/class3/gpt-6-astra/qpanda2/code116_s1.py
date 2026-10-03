# EVAL_META: task_id=116, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq
from scipy.linalg import expm

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
atexit.register(machine.finalize)


def synthesize_evolution_gate(pauli_string, time):
    if not isinstance(pauli_string, str) or not pauli_string:
        raise ValueError("pauli_string must be a nonempty string.")
    if any(symbol not in "IXYZ" for symbol in pauli_string):
        raise ValueError("pauli_string may contain only I, X, Y, and Z.")

    while len(qubits) < len(pauli_string):
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()
    basis = pq.QCircuit()
    active = []

    # Qiskit's rightmost Pauli character acts on qubit zero.
    for index, symbol in enumerate(reversed(pauli_string)):
        if symbol == "I":
            continue
        qubit = qubits[index]
        active.append(qubit)
        if symbol == "X":
            basis << pq.H(qubit)
        elif symbol == "Y":
            basis << pq.RX(qubit, np.pi / 2)

    if active:
        parity = pq.QCircuit()
        target = active[-1]
        for control in active[:-1]:
            parity << pq.CNOT(control, target)

        evolution = expm(
            -1j * float(time) * np.diag([1.0, -1.0])
        )
        circuit << basis
        circuit << parity
        circuit << pq.QOracle([target], evolution.ravel().tolist())
        circuit << parity.dagger()
        circuit << basis.dagger()
    else:
        # Preserve the global phase of exp(-i * time * I).
        evolution = expm(-1j * float(time) * np.eye(2))
        circuit << pq.QOracle([qubits[0]], evolution.ravel().tolist())

    # Retain idle qubits in the returned circuit.
    for qubit in qubits[:len(pauli_string)]:
        circuit << pq.I(qubit)

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
