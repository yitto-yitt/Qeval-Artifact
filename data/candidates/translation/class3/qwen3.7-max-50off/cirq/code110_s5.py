# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import random

def equivalent_clifford_circuit(circuit, n):
    qc_list = []
    qubits = sorted(circuit.all_qubits())
    gates = [cirq.X, cirq.Y, cirq.Z, cirq.H]
    for i in range(n):
        c = circuit.copy()
        if qubits:
            num_pairs = random.randint(1, 5)
            for _ in range(num_pairs):
                q = random.choice(qubits)
                g = random.choice(gates)
                c.append(g(q))
                c.append(g(q))
        qc_list.append(c)
    return qc_list
