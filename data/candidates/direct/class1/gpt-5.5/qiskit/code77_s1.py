# EVAL_META: task_id=77, framework=qiskit, class=1
import math
from qiskit import QuantumCircuit


def circuit_from_probability_dist(probability_dist):
    def normalize_key(key):
        if isinstance(key, str):
            s = key.strip().replace(" ", "").replace("_", "")
            if s.startswith(("0b", "0B")):
                s = s[2:]
            return s
        if isinstance(key, int):
            if key < 0:
                raise ValueError("Measurement keys must be non-negative.")
            return bin(key)[2:]
        if isinstance(key, (tuple, list)):
            return "".join(str(int(b)) for b in key)
        return str(key)

    if not probability_dist:
        raise ValueError("probability_dist must not be empty.")

    raw_keys = [normalize_key(k) for k in probability_dist.keys()]

    if all(k == "" for k in raw_keys):
        return QuantumCircuit(0, 0)

    n_qubits = max(1, max(len(k) for k in raw_keys))
    dim = 1 << n_qubits
    probabilities = [0.0] * dim

    for original_key, prob in probability_dist.items():
        key = normalize_key(original_key)
        if len(key) > n_qubits:
            raise ValueError("Inconsistent measurement key lengths.")
        if any(ch not in "01" for ch in key):
            raise ValueError("Measurement keys must be bitstrings.")
        padded_key = key.zfill(n_qubits)
        index = int(padded_key, 2)
        probabilities[index] += float(prob)

    total = sum(probabilities)
    if total <= 0:
        raise ValueError("Total probability must be positive.")

    amplitudes = [math.sqrt(max(p, 0.0) / total) for p in probabilities]

    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.initialize(amplitudes, list(range(n_qubits)))
    qc.measure(list(range(n_qubits)), list(range(n_qubits)))
    return qc
