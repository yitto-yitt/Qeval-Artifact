# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np


def dj_algorithm(oracle):
    qubits = sorted(oracle.all_qubits())
    n = len(qubits)
    input_qubits = qubits[:-1]
    output_qubit = qubits[-1]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(output_qubit))
    circuit.append([cirq.H(q) for q in qubits])
    circuit.append(oracle.all_operations())
    circuit.append([cirq.H(q) for q in qubits])

    result = cirq.Simulator().simulate(circuit, qubit_order=qubits)
    sv = result.final_state_vector
    probs = np.abs(sv) ** 2

    dist = {}
    for idx, p in enumerate(probs):
        if p <= 1e-12:
            continue
        bits = [(idx >> (n - 1 - i)) & 1 for i in range(n)]
        input_bits = bits[:-1]  # qubits[0..n-2]
        # Qiskit-style bitstring: highest classical index first
        key = ''.join(str(b) for b in reversed(input_bits))
        dist[key] = dist.get(key, 0.0) + float(p)

    total = sum(dist.values())
    return {k: v / total for k, v in dist.items()}
