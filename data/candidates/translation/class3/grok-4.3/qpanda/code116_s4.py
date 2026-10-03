# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import QProg, qAlloc_many, H, S, Sdag, RZ, CNOT

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    prog = QProg()
    qubits = qAlloc_many(n)
    z_qubits = []
    for i, p in enumerate(pauli_string):
        if p == 'X':
            prog << H(qubits[i])
            z_qubits.append(qubits[i])
        elif p == 'Y':
            prog << Sdag(qubits[i]) << H(qubits[i])
            z_qubits.append(qubits[i])
        elif p == 'Z':
            z_qubits.append(qubits[i])
    if not z_qubits:
        return prog
    target = z_qubits[-1]
    for q in z_qubits[:-1]:
        prog << CNOT(q, target)
    prog << RZ(target, 2 * time)
    for q in reversed(z_qubits[:-1]):
        prog << CNOT(q, target)
    for i, p in enumerate(pauli_string):
        if p == 'X':
            prog << H(qubits[i])
        elif p == 'Y':
            prog << H(qubits[i]) << S(qubits[i])
    return prog
