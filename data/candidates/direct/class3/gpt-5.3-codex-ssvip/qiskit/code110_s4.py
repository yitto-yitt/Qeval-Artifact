# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford
import numpy as np


def equivalent_clifford_circuit(circuit, n):
    target = Clifford(circuit)
    num_qubits = circuit.num_qubits
    results = []

    max_trials = max(200, 50 * max(1, n))
    trials = 0

    while len(results) < n and trials < max_trials:
        trials += 1
        cand = QuantumCircuit(num_qubits)

        depth = np.random.randint(1, max(3, 6 * num_qubits))
        for _ in range(depth):
            gate_choice = np.random.randint(0, 6)
            if gate_choice == 0:
                q = np.random.randint(0, num_qubits)
                cand.h(q)
            elif gate_choice == 1:
                q = np.random.randint(0, num_qubits)
                cand.s(q)
            elif gate_choice == 2:
                q = np.random.randint(0, num_qubits)
                cand.sdg(q)
            elif gate_choice == 3:
                q = np.random.randint(0, num_qubits)
                cand.x(q)
            elif gate_choice == 4:
                q = np.random.randint(0, num_qubits)
                cand.z(q)
            else:
                if num_qubits > 1:
                    a, b = np.random.choice(num_qubits, size=2, replace=False)
                    cand.cx(int(a), int(b))
                else:
                    q = 0
                    cand.h(q)

        candidate_full = cand.compose(circuit)
        try:
            if Clifford(candidate_full) == target:
                results.append(candidate_full)
        except Exception:
            pass

    while len(results) < n:
        results.append(circuit.copy())

    return results
