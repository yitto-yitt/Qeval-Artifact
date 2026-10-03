# EVAL_META: task_id=77, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit


def circuit_from_probability_dist(probability_dist):
    keys = list(probability_dist.keys())
    if not keys:
        qc = QuantumCircuit(1)
        qc.measure_all()
        return qc

    sample_key = keys[0]

    if isinstance(sample_key, str):
        clean_keys = [str(k).strip() for k in keys]
        num_qubits = max(len(k) for k in clean_keys)

        def _to_index(k):
            return int(str(k).strip(), 2)

    elif isinstance(sample_key, int):
        max_idx = max(keys)
        num_qubits = max(1, int(np.ceil(np.log2(max_idx + 1))))

        def _to_index(k):
            return int(k)

    else:
        clean_keys = [str(k).strip() for k in keys]
        num_qubits = max(len(k) for k in clean_keys)

        def _to_index(k):
            return int(str(k).strip(), 2)

    statevector = np.zeros(2 ** num_qubits, dtype=complex)

    for ket, prob in probability_dist.items():
        idx = _to_index(ket)
        statevector[idx] = np.sqrt(prob)

    norm = np.linalg.norm(statevector)
    if norm > 0:
        statevector = statevector / norm

    qc = QuantumCircuit(num_qubits)
    qc.prepare_state(statevector, qc.qubits)
    qc.measure_all()

    return qc
