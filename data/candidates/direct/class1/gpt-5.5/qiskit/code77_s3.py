# EVAL_META: task_id=77, framework=qiskit, class=1
import math
import numpy as np
from qiskit import QuantumCircuit


def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        return QuantumCircuit(0)

    normalized_items = []
    max_width = 0

    for measurement, probability in probability_dist.items():
        if isinstance(measurement, int):
            bits = bin(measurement)[2:]
        else:
            bits = str(measurement).replace(" ", "")
            if bits.startswith("0b"):
                bits = bits[2:]
            elif bits.startswith("0x"):
                bits = bin(int(bits, 16))[2:]
        if bits == "":
            bits = "0"
        max_width = max(max_width, len(bits))
        normalized_items.append((bits, float(probability)))

    num_qubits = max_width
    dimension = 2 ** num_qubits
    probabilities = np.zeros(dimension, dtype=float)

    for bits, probability in normalized_items:
        padded_bits = bits.zfill(num_qubits)
        index = int(padded_bits, 2)
        probabilities[index] += probability

    total_probability = float(np.sum(probabilities))
    if total_probability <= 0:
        probabilities[0] = 1.0
    else:
        probabilities /= total_probability

    amplitudes = np.sqrt(probabilities).astype(complex)

    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.initialize(amplitudes, range(num_qubits))
    qc.measure(range(num_qubits), range(num_qubits))
    return qc
