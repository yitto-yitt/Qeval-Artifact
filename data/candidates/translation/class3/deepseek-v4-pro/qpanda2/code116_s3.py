# EVAL_META: task_id=116, framework=qpanda2, class=3
from pyqpanda import *
import math

machine = CPUQVM()
machine.init_qvm()

def synthesize_evolution_gate(pauli_string, time):
    pauli_string = str(pauli_string).strip().upper()
    n = len(pauli_string)
    qubits = machine.qAlloc_many(n)
    circuit = QCircuit()

    non_i = [i for i, ch in enumerate(pauli_string) if ch != 'I']
    if not non_i:
        return circuit

    for i in non_i:
        ch = pauli_string[i]
        if ch == 'X':
            circuit.insert(H(qubits[i]))
        elif ch == 'Y':
            circuit.insert(RX(qubits[i], math.pi / 2))

    for k in range(len(non_i) - 1):
        circuit.insert(CNOT(qubits[non_i[k]], qubits[non_i[k + 1]]))

    circuit.insert(RZ(qubits[non_i[-1]], 2 * time))

    for k in range(len(non_i) - 2, -1, -1):
        circuit.insert(CNOT(qubits[non_i[k]], qubits[non_i[k + 1]]))

    for i in reversed(non_i):
        ch = pauli_string[i]
        if ch == 'X':
            circuit.insert(H(qubits[i]))
        elif ch == 'Y':
            circuit.insert(RX(qubits[i], -math.pi / 2))

    return circuit

machine.finalize()
