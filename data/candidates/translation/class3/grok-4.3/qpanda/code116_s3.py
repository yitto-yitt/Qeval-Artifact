# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qc = QuantumCircuit(n)
    active_qubits = [i for i, p in enumerate(pauli_string) if p != 'I']
    for i, p in enumerate(pauli_string):
        if p == 'X':
            qc.h(i)
        elif p == 'Y':
            qc.sdg(i)
            qc.h(i)
    if active_qubits:
        for i in range(len(active_qubits) - 1):
            qc.cx(active_qubits[i], active_qubits[i + 1])
        qc.rz(active_qubits[-1], 2 * time)
        for i in range(len(active_qubits) - 2, -1, -1):
            qc.cx(active_qubits[i], active_qubits[i + 1])
    for i, p in enumerate(pauli_string):
        if p == 'X':
            qc.h(i)
        elif p == 'Y':
            qc.h(i)
            qc.s(i)
    return qc
