# EVAL_META: task_id=77, framework=qiskit, class=1
from numbers import Integral

import numpy as np
from qiskit import QuantumCircuit


def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        raise ValueError("probability_dist must not be empty.")

    indexed_probabilities = {}
    num_qubits = 1

    for measurement, probability in probability_dist.items():
        if isinstance(measurement, str):
            bits = "".join(measurement.split())
            if bits.startswith(("0b", "0B")):
                bits = bits[2:]
            if not bits or any(bit not in "01" for bit in bits):
                raise ValueError("Measurement strings must contain binary digits.")
            index = int(bits, 2)
            num_qubits = max(num_qubits, len(bits))
        elif isinstance(measurement, Integral):
            index = int(measurement)
            if index < 0:
                raise ValueError("Measurement indices must be nonnegative.")
            num_qubits = max(num_qubits, index.bit_length())
        else:
            raise TypeError("Measurements must be binary strings or integers.")

        value = float(probability)
        if not np.isfinite(value) or value < 0:
            raise ValueError("Probabilities must be finite and nonnegative.")
        indexed_probabilities[index] = indexed_probabilities.get(index, 0.0) + value

    scale = max(indexed_probabilities.values())
    if scale <= 0 or not np.isfinite(scale):
        raise ValueError("The distribution must have finite positive total weight.")

    probabilities = np.zeros(1 << num_qubits, dtype=float)
    for index, value in indexed_probabilities.items():
        probabilities[index] = value / scale
    probabilities /= probabilities.sum()

    circuit = QuantumCircuit(num_qubits)
    circuit.initialize(np.sqrt(probabilities), range(num_qubits))
    circuit.measure_all()
    return circuit
