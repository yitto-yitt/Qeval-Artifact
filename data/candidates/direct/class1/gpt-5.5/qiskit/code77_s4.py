# EVAL_META: task_id=77, framework=qiskit, class=1
from math import sqrt
from qiskit import QuantumCircuit


def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        return QuantumCircuit(0)

    def key_to_bitstring(key):
        if isinstance(key, str):
            s = key.strip().replace(" ", "").replace("_", "")
            if s.startswith(("0b", "0B")):
                s = s[2:]
            elif s.startswith(("0x", "0X")):
                s = bin(int(s, 16))[2:]
            return s
        if isinstance(key, int):
            return bin(key)[2:] if key > 0 else "0"
        if isinstance(key, (tuple, list)):
            return "".join(str(int(x)) for x in key)
        return str(key).strip().replace(" ", "").replace("_", "")

    raw_items = [(key_to_bitstring(k), float(v)) for k, v in probability_dist.items()]
    n_qubits = max(len(bits) for bits, _ in raw_items)
    if n_qubits == 0:
        return QuantumCircuit(0)

    probabilities = {}
    for bits, prob in raw_items:
        bits = bits.zfill(n_qubits)
        probabilities[bits] = probabilities.get(bits, 0.0) + max(0.0, prob)

    total = sum(probabilities.values())
    if total <= 0.0:
        probabilities = {"0" * n_qubits: 1.0}
        total = 1.0

    amplitudes = [0.0] * (2 ** n_qubits)
    for bits, prob in probabilities.items():
        index = int(bits, 2)
        amplitudes[index] = sqrt(prob / total)

    circuit = QuantumCircuit(n_qubits)
    circuit.initialize(amplitudes, range(n_qubits))
    return circuit
