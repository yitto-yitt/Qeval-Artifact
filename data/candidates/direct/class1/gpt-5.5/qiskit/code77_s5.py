# EVAL_META: task_id=77, framework=qiskit, class=1
import math

from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation


def circuit_from_probability_dist(probability_dist):
    def _clean_key(key):
        if isinstance(key, str):
            s = key.replace(" ", "").replace("_", "")
            if s.startswith(("0x", "0X")):
                idx = int(s, 16)
                return idx, max(1, idx.bit_length()), False
            if s == "":
                return 0, 0, True
            return int(s, 2), len(s), True
        if isinstance(key, int):
            return int(key), max(1, int(key).bit_length()), False
        if isinstance(key, (tuple, list)):
            s = "".join(str(int(b)) for b in key)
            if s == "":
                return 0, 0, True
            return int(s, 2), len(s), True
        s = str(key).replace(" ", "").replace("_", "")
        if s == "":
            return 0, 0, True
        return int(s, 2), len(s), True

    if not probability_dist:
        return QuantumCircuit(0)

    parsed = []
    width = 0
    has_explicit_width = False

    for key, probability in probability_dist.items():
        index, key_width, explicit_width = _clean_key(key)
        parsed.append((index, float(probability)))
        width = max(width, key_width)
        has_explicit_width = has_explicit_width or explicit_width

    if not has_explicit_width:
        max_index = max(index for index, _ in parsed)
        width = max(1, max_index.bit_length())

    num_qubits = width
    qc = QuantumCircuit(num_qubits)

    if num_qubits == 0:
        return qc

    dimension = 1 << num_qubits
    probabilities = [0.0] * dimension

    for index, probability in parsed:
        if 0 <= index < dimension:
            probabilities[index] += probability

    total = sum(probabilities)
    if total <= 0.0:
        probabilities[0] = 1.0
        total = 1.0

    amplitudes = [math.sqrt(max(0.0, p / total)) for p in probabilities]
    qc.append(StatePreparation(amplitudes), range(num_qubits))
    return qc
