# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, QProg, H, RX, RZ, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(64)


def _pauli_evolution(pauli_string, time, reps):
    n = len(pauli_string)
    circ = QCircuit()
    # Qiskit qubit ordering: pauli_string[i] acts on qubit (n-1-i)
    active = []
    for i, p in enumerate(pauli_string):
        q = n - 1 - i
        if p != 'I':
            active.append((q, p))
    if not active:
        return circ

    angle = 2.0 * time / reps

    for _ in range(reps):
        rep = QCircuit()
        # basis change to Z
        for q, p in active:
            if p == 'X':
                rep << H(qubits[q])
            elif p == 'Y':
                rep << RX(qubits[q], 1.5707963267948966)
        # CNOT ladder
        targets = [q for q, _ in active]
        for k in range(len(targets) - 1):
            rep << CNOT(qubits[targets[k]], qubits[targets[k + 1]])
        # rotation on last qubit
        rep << RZ(qubits[targets[-1]], angle)
        # uncompute ladder
        for k in range(len(targets) - 1, 0, -1):
            rep << CNOT(qubits[targets[k - 1]], qubits[targets[k]])
        # undo basis change
        for q, p in active:
            if p == 'X':
                rep << H(qubits[q])
            elif p == 'Y':
                rep << RX(qubits[q], -1.5707963267948966)
        circ << rep
    return circ


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    prog = QProg()
    circuit = QCircuit()
    for pauli_string, time in zip(pauli_strings, times):
        circuit << _pauli_evolution(pauli_string, time, reps)
    prog << circuit
    return prog
