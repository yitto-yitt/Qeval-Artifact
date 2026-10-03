# EVAL_META: task_id=116, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
import atexit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)
atexit.register(machine.finalize)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    if n > len(qubits):
        raise ValueError("Pauli string length exceeds globally allocated qubit pool.")

    qs = qubits[:n]
    circuit = QCircuit()
    active = []

    for i, pauli in enumerate(pauli_string):
        qidx = n - 1 - i
        if pauli == "I":
            circuit << H(qs[qidx])
            circuit << H(qs[qidx])
        elif pauli == "X":
            circuit << H(qs[qidx])
            active.append(qidx)
        elif pauli == "Y":
            circuit << RX(qs[qidx], np.pi / 2)
            active.append(qidx)
        elif pauli == "Z":
            active.append(qidx)
        else:
            raise ValueError("Pauli string can only contain 'I', 'X', 'Y', and 'Z'.")

    if active:
        target = active[-1]

        for qidx in active[:-1]:
            circuit << CNOT(qs[qidx], qs[target])

        circuit << RZ(qs[target], 2 * time)

        for qidx in reversed(active[:-1]):
            circuit << CNOT(qs[qidx], qs[target])

    for i in reversed(range(n)):
        pauli = pauli_string[i]
        qidx = n - 1 - i
        if pauli == "X":
            circuit << H(qs[qidx])
        elif pauli == "Y":
            circuit << RX(qs[qidx], -np.pi / 2)

    return circuit
