# EVAL_META: task_id=112, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(64)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = _global_qubits[:n]
    prog = pq.QProg()

    def apply_pauli_evolution(pauli_str, t):
        nonlocal prog
        active = []
        for i, p in enumerate(pauli_str):
            if p != 'I':
                active.append(i)
                if p == 'X':
                    prog << pq.H(qubits[i])
                elif p == 'Y':
                    prog << pq.RX(qubits[i], 1.5707963267948966)

        if len(active) == 0:
            return

        if len(active) == 1:
            q = qubits[active[0]]
            prog << pq.RZ(q, 2.0 * t)
        else:
            for k in range(len(active) - 1):
                prog << pq.CNOT(qubits[active[k]], qubits[active[k + 1]])
            prog << pq.RZ(qubits[active[-1]], 2.0 * t)
            for k in range(len(active) - 2, -1, -1):
                prog << pq.CNOT(qubits[active[k]], qubits[active[k + 1]])

        for i in reversed(active):
            p = pauli_str[i]
            if p == 'X':
                prog << pq.H(qubits[i])
            elif p == 'Y':
                prog << pq.RX(qubits[i], -1.5707963267948966)

    for _ in range(reps):
        for pauli_string, t in zip(pauli_strings, times):
            apply_pauli_evolution(pauli_string, t)

    return prog

machine.finalize()
