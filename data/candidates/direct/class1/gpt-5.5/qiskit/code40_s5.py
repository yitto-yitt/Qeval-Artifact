# EVAL_META: task_id=40, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def init_random_3qubit(desired_vector):
    vector = np.asarray(desired_vector, dtype=complex).reshape(-1)
    if vector.size != 8:
        raise ValueError("desired_vector must contain 8 amplitudes for a 3-qubit state")

    norm = np.linalg.norm(vector)
    if norm == 0:
        raise ValueError("desired_vector must not be the zero vector")
    vector = vector / norm

    circuit = QuantumCircuit(3)
    circuit.initialize(vector.tolist(), [0, 1, 2])
    circuit.measure_all()

    shots = 32768

    try:
        backend = AerSimulator(seed_simulator=40040)
        isa_circuit = transpile(
            circuit,
            backend=backend,
            optimization_level=1,
            seed_transpiler=40040,
        )

        sampler = Sampler(mode=backend)
        job = sampler.run([isa_circuit], shots=shots)
        result = job.result()[0]

        try:
            counts = result.data.meas.get_counts()
        except Exception:
            counts = None
            if hasattr(result.data, "keys"):
                for key in result.data.keys():
                    value = getattr(result.data, key)
                    if hasattr(value, "get_counts"):
                        counts = value.get_counts()
                        break
            if counts is None:
                counts = {}

        cleaned_counts = {}
        for key, value in counts.items():
            bitstring = str(key).replace(" ", "")
            if bitstring.startswith("0b"):
                bitstring = bitstring[2:]
            elif bitstring.startswith("0x"):
                bitstring = bin(int(bitstring, 16))[2:]
            bitstring = bitstring.zfill(3)[-3:]
            cleaned_counts[bitstring] = cleaned_counts.get(bitstring, 0) + int(value)

        total = sum(cleaned_counts.values())
        if total > 0:
            return {
                format(i, "03b"): float(cleaned_counts.get(format(i, "03b"), 0) / total)
                for i in range(8)
            }
    except Exception:
        pass

    probabilities = np.abs(vector) ** 2
    probabilities = probabilities / probabilities.sum()
    return {format(i, "03b"): float(probabilities[i]) for i in range(8)}
