# EVAL_META: task_id=116, framework=qpanda2, class=3
import math
import atexit
import pyqpanda as pq

_MAX_QUBITS = 64

machine = pq.CPUQVM()
try:
    machine.set_configure(_MAX_QUBITS, _MAX_QUBITS)
except Exception:
    pass
machine.init_qvm()
qubits = machine.qAlloc_many(_MAX_QUBITS)


def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    if n > _MAX_QUBITS:
        raise ValueError("pauli_string is longer than the globally allocated qubit register")

    labels_by_qubit = pauli_string[::-1]
    for label in labels_by_qubit:
        if label not in ("I", "X", "Y", "Z"):
            raise ValueError("Invalid Pauli character")

    circuit = pq.QCircuit()
    active = [idx for idx, label in enumerate(labels_by_qubit) if label != "I"]

    for idx, label in enumerate(labels_by_qubit):
        if label == "X":
            circuit << pq.H(qubits[idx])
        elif label == "Y":
            circuit << pq.RZ(qubits[idx], -math.pi / 2)
            circuit << pq.H(qubits[idx])

    if active:
        target = active[-1]
        for control in active[:-1]:
            circuit << pq.CNOT(qubits[control], qubits[target])

        circuit << pq.RZ(qubits[target], 2 * time)

        for control in reversed(active[:-1]):
            circuit << pq.CNOT(qubits[control], qubits[target])

    for idx in reversed(range(n)):
        label = labels_by_qubit[idx]
        if label == "X":
            circuit << pq.H(qubits[idx])
        elif label == "Y":
            circuit << pq.H(qubits[idx])
            circuit << pq.RZ(qubits[idx], math.pi / 2)

    return circuit


atexit.register(machine.finalize)
