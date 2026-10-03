# EVAL_META: task_id=112, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(30)


def _append_pauli_evolution(prog, pauli_string, time, qubits, reps):
    n = len(pauli_string)
    # qiskit convention: pauli_string[0] is the highest qubit index
    # map: char at index i corresponds to qubit (n-1-i)
    active = [(n - 1 - i, ch) for i, ch in enumerate(pauli_string) if ch != 'I']
    if not active:
        return
    dt = time / reps
    for _ in range(reps):
        # basis change
        for q, ch in active:
            if ch == 'X':
                prog << pq.H(qubits[q])
            elif ch == 'Y':
                prog << pq.RX(qubits[q], 3.141592653589793 / 2)
        # CNOT ladder
        idxs = [q for q, ch in active]
        for k in range(len(idxs) - 1):
            prog << pq.CNOT(qubits[idxs[k]], qubits[idxs[k + 1]])
        # RZ rotation on last qubit
        prog << pq.RZ(qubits[idxs[-1]], 2.0 * dt)
        # undo CNOT ladder
        for k in reversed(range(len(idxs) - 1)):
            prog << pq.CNOT(qubits[idxs[k]], qubits[idxs[k + 1]])
        # undo basis change
        for q, ch in active:
            if ch == 'X':
                prog << pq.H(qubits[q])
            elif ch == 'Y':
                prog << pq.RX(qubits[q], -3.141592653589793 / 2)


def create_product_formula_circuit(pauli_strings, times, order, reps):
    prog = pq.QProg()
    for pauli_string, time in zip(pauli_strings, times):
        _append_pauli_evolution(prog, pauli_string, time, qubits, reps)
    return prog


if __name__ == "__main__":
    circuit = create_product_formula_circuit(["XYZ", "ZZI"], [0.5, 0.3], 1, 1)
    print(circuit)
    machine.finalize()
