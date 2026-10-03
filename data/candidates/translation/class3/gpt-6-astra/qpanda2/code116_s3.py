# EVAL_META: task_id=116, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
atexit.register(machine.finalize)


def synthesize_evolution_gate(pauli_string, time):
    if not isinstance(pauli_string, str) or not pauli_string:
        raise ValueError("pauli_string must be a nonempty string.")
    if any(p not in "IXYZ" for p in pauli_string):
        raise ValueError("pauli_string must contain only I, X, Y, and Z.")

    n = len(pauli_string)
    while len(qubits) < n:
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()
    basis = pq.QCircuit()
    active = []

    for index, pauli in enumerate(reversed(pauli_string)):
        qubit = qubits[index]
        circuit << pq.I(qubit)
        if pauli != "I":
            active.append(qubit)
        if pauli == "X":
            basis << pq.H(qubit)
        elif pauli == "Y":
            basis << pq.RX(qubit, np.pi / 2)

    if active:
        parity = pq.QCircuit()
        target = active[-1]
        for control in active[:-1]:
            parity << pq.CNOT(control, target)

        circuit << basis
        circuit << parity
        circuit << pq.RZ(target, 2 * float(time))
        circuit << parity.dagger()
        circuit << basis.dagger()
    else:
        phase = complex(np.exp(-1j * float(time)))
        circuit << pq.QOracle(
            [qubits[0]], [phase, 0j, 0j, phase]
        )

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
