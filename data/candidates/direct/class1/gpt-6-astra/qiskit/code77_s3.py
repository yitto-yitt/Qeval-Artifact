# EVAL_META: task_id=77, framework=qiskit, class=1
import math
import operator

import numpy as np
from qiskit import QuantumCircuit


def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        raise ValueError("The probability distribution must not be empty.")

    probabilities = {}
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
        else:
            index = operator.index(measurement)
            if index < 0:
                raise ValueError("Measurement indices must be nonnegative.")
            num_qubits = max(num_qubits, index.bit_length())

        probability = float(probability)
        if not math.isfinite(probability) or probability < 0:
            raise ValueError("Probabilities must be finite and nonnegative.")

        probabilities[index] = probabilities.get(index, 0.0) + probability

    total = math.fsum(probabilities.values())
    if not math.isfinite(total) or total <= 0:
        raise ValueError("The total probability must be finite and positive.")

    amplitudes = np.zeros(1 << num_qubits, dtype=complex)
    for index, probability in probabilities.items():
        amplitudes[index] = math.sqrt(probability / total)

    circuit = QuantumCircuit(num_qubits)
    circuit.initialize(amplitudes, range(num_qubits))
    circuit.measure_all()
    return circuit
