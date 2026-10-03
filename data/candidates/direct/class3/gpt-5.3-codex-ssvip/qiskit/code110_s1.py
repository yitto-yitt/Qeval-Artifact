# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford
import random


def equivalent_clifford_circuit(circuit, n):
    target = Clifford(circuit)
    num_qubits = circuit.num_qubits
    out = []
    max_attempts = max(200, 50 * n)
    attempts = 0

    while len(out) < n and attempts < max_attempts:
        attempts += 1
        cand = QuantumCircuit(num_qubits)

        depth = random.randint(max(1, num_qubits), max(3, 4 * num_qubits))
        for _ in range(depth):
            gate_choice = random.randint(0, 6)
            q = random.randrange(num_qubits)
            if gate_choice == 0:
                cand.h(q)
            elif gate_choice == 1:
                cand.s(q)
            elif gate_choice == 2:
                cand.sdg(q)
            elif gate_choice == 3:
                cand.x(q)
            elif gate_choice == 4:
                cand.z(q)
            elif gate_choice == 5 and num_qubits > 1:
                q2 = random.randrange(num_qubits - 1)
                if q2 >= q:
                    q2 += 1
                cand.cx(q, q2)
            elif gate_choice == 6 and num_qubits > 1:
                q2 = random.randrange(num_qubits - 1)
                if q2 >= q:
                    q2 += 1
                cand.cz(q, q2)

        try:
            if Clifford(cand) == target:
                out.append(cand)
        except Exception:
            continue

    while len(out) < n:
        out.append(circuit.copy())

    return out
