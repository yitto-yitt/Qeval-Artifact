# EVAL_META: task_id=112, framework=qpanda, class=3
import math
import pyqpanda3.core as pq

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0]) if pauli_strings else 0

    qvm = pq.CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    qubits = qvm.qAlloc_many(n)
    circuit = pq.QCircuit()

    if not hasattr(create_product_formula_circuit, "_qvms"):
        create_product_formula_circuit._qvms = []
    create_product_formula_circuit._qvms.append(qvm)

    def add(gate):
        nonlocal circuit
        try:
            circuit << gate
        except Exception:
            circuit.insert(gate)

    def h(q):
        return pq.H(q)

    def rx(q, a):
        return pq.RX(q, a)

    def rz(q, a):
        return pq.RZ(q, a)

    def cnot(c, t):
        if hasattr(pq, "CNOT"):
            return pq.CNOT(c, t)
        return pq.CX(c, t)

    for pauli_string, time in zip(pauli_strings, times):
        dt = float(time) / reps
        for _ in range(reps):
            active = []
            for i, p in enumerate(pauli_string):
                p = p.upper()
                if p != "I":
                    q_index = n - 1 - i
                    q = qubits[q_index]
                    active.append((q_index, q, p))
                    if p == "X":
                        add(h(q))
                    elif p == "Y":
                        add(rx(q, -math.pi / 2.0))

            if active:
                ordered = [item[1] for item in sorted(active, key=lambda x: x[0])]
                for j in range(len(ordered) - 1):
                    add(cnot(ordered[j], ordered[j + 1]))

                add(rz(ordered[-1], 2.0 * dt))

                for j in range(len(ordered) - 2, -1, -1):
                    add(cnot(ordered[j], ordered[j + 1]))

                for _, q, p in reversed(active):
                    if p == "X":
                        add(h(q))
                    elif p == "Y":
                        add(rx(q, math.pi / 2.0))

    return circuit
