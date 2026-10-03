# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, H, S, SDAG, RZ, CNOT

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    circuit = QCircuit()
    qubits = [Qubit(i) for i in range(n)]
    active = []
    for i, p in enumerate(pauli_string):
        if p != 'I':
            active.append(i)
            if p == 'X':
                circuit << H(qubits[i])
            elif p == 'Y':
                circuit << SDAG(qubits[i]) << H(qubits[i])
    if not active:
        return circuit
    tgt = active[-1]
    for ctrl in reversed(active[:-1]):
        circuit << CNOT(qubits[ctrl], qubits[tgt])
    circuit << RZ(qubits[tgt], 2 * time)
    for ctrl in active[:-1]:
        circuit << CNOT(qubits[ctrl], qubits[tgt])
    for i in reversed(active):
        p = pauli_string[i]
        if p == 'X':
            circuit << H(qubits[i])
        elif p == 'Y':
            circuit << H(qubits[i]) << S(qubits[i])
    return circuit
