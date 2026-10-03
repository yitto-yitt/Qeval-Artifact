# EVAL_META: task_id=116, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(29)
atexit.register(lambda: machine.finalize())


def synthesize_evolution_gate(pauli_string, time):
    if not isinstance(pauli_string, str) or not pauli_string:
        raise ValueError("pauli_string must be a nonempty string.")
    if any(p not in "IXYZ" for p in pauli_string):
        raise ValueError("pauli_string may contain only I, X, Y, and Z.")
    if len(pauli_string) > len(qubits):
        raise ValueError("The Pauli string exceeds the available qubit count.")

    time = float(time)
    labels = list(reversed(pauli_string))
    circuit = pq.QCircuit()

    for index in range(len(labels)):
        circuit << pq.RZ(qubits[index], 0.0)

    active = [index for index, label in enumerate(labels) if label != "I"]

    if not active:
        q = qubits[0]
        circuit << pq.U1(q, -time)
        circuit << pq.X(q)
        circuit << pq.U1(q, -time)
        circuit << pq.X(q)
    else:
        for index in active:
            if labels[index] == "X":
                circuit << pq.H(qubits[index])
            elif labels[index] == "Y":
                circuit << pq.RX(qubits[index], np.pi / 2)

        target = qubits[active[-1]]
        for index in active[:-1]:
            circuit << pq.CNOT(qubits[index], target)

        circuit << pq.RZ(target, 2.0 * time)

        for index in reversed(active[:-1]):
            circuit << pq.CNOT(qubits[index], target)

        for index in reversed(active):
            if labels[index] == "X":
                circuit << pq.H(qubits[index])
            elif labels[index] == "Y":
                circuit << pq.RX(qubits[index], -np.pi / 2)

    program = pq.QProg()
    program << circuit
    pq.get_matrix(program)
    return circuit
