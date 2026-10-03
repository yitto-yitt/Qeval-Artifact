# EVAL_META: task_id=116, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
MAX_QUBITS = 20
q = machine.qAlloc_many(MAX_QUBITS)

def synthesize_evolution_gate(pauli_string, time):
    pauli_string = pauli_string.upper()
    n = len(pauli_string)
    circuit = pq.QCircuit()
    indices = [i for i, p in enumerate(pauli_string) if p != 'I']

    if not indices:
        return circuit

    for i in indices:
        if pauli_string[i] == 'X':
            circuit.insert(pq.H(q[i]))
        elif pauli_string[i] == 'Y':
            circuit.insert(pq.RX(q[i], np.pi / 2))

    for j in range(len(indices) - 1):
        circuit.insert(pq.CNOT(q[indices[j]], q[indices[j + 1]]))

    target = indices[-1]
    circuit.insert(pq.RZ(q[target], 2 * time))

    for j in reversed(range(len(indices) - 1)):
        circuit.insert(pq.CNOT(q[indices[j]], q[indices[j + 1]]))

    for i in reversed(indices):
        if pauli_string[i] == 'X':
            circuit.insert(pq.H(q[i]))
        elif pauli_string[i] == 'Y':
            circuit.insert(pq.RX(q[i], -np.pi / 2))

    return circuit

machine.finalize()
