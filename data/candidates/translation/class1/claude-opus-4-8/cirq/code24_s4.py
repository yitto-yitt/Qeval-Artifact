# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np


def dj_algorithm(oracle):
    oracle_qubits = sorted(oracle.all_qubits())
    n = len(oracle_qubits)
    qubits = cirq.LineQubit.range(n)

    mapping = {oq: qubits[i] for i, oq in enumerate(oracle_qubits)}
    oracle_mapped = oracle.transform_qubits(mapping)

    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[n - 1]))
    circuit.append(cirq.H(q) for q in qubits)
    circuit += oracle_mapped
    circuit.append(cirq.H(q) for q in qubits)

    result = cirq.Simulator().simulate(circuit, qubit_order=qubits)
    state = result.final_state_vector
    probs = np.abs(state) ** 2

    dist = {}
    for idx, p in enumerate(probs):
        if np.isclose(p, 0.0):
            continue
        bits = [(idx >> (n - 1 - i)) & 1 for i in range(n)]
        key = ''.join(str(bits[i]) for i in reversed(range(n - 1)))
        dist[key] = dist.get(key, 0.0) + float(p)

    total = sum(dist.values())
    return {k: v / total for k, v in dist.items()}
