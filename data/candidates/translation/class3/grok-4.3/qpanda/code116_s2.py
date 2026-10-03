# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, H, S, Sdag, CNOT, RZ

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qubits = [Qubit(i) for i in range(n)]
    circuit = QCircuit()
    active = [i for i in range(n) if pauli_string[i] != 'I']
    if not active:
        return circuit
    for q in active:
        p = pauli_string[q]
        if p == 'X':
            circuit << H(qubits[q])
        elif p == 'Y':
            circuit << Sdag(qubits[q]) << H(qubits[q])
    target = active[-1]
    for i in range(len(active) - 1):
        ctrl = active[i]
        tgt = active[i + 1]
        circuit << CNOT(qubits[ctrl], qubits[tgt])
    circuit << RZ(qubits[target], 2 * time)
    for i in reversed(range(len(active) - 1)):
        ctrl = active[i]
        tgt = active[i + 1]
        circuit << CNOT(qubits[ctrl], qubits[tgt])
    for q in reversed(active):
        p = pauli_string[q]
        if p == 'X':
            circuit << H(qubits[q])
        elif p == 'Y':
            circuit << H(qubits[q]) << S(qubits[q])
    return circuit
