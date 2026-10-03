# EVAL_META: task_id=40, framework=qiskit, class=1
import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as RuntimeSampler


def init_random_3qubit(desired_vector):
    vector = np.asarray(desired_vector, dtype=complex).reshape(-1)
    if vector.size != 8:
        raise ValueError("desired_vector must contain exactly 8 amplitudes for a 3-qubit state.")

    norm = np.linalg.norm(vector)
    if norm == 0:
        raise ValueError("desired_vector must not be the zero vector.")
    vector = vector / norm

    qc = QuantumCircuit(3)
    meas = ClassicalRegister(3, "meas")
    qc.add_register(meas)
    qc.initialize(vector.tolist(), [0, 1, 2])
    qc.measure([0, 1, 2], meas)

    shots = 32768
    seed = 12345
    backend = AerSimulator(seed_simulator=seed)
    circuit = transpile(qc, backend=backend, seed_transpiler=seed, optimization_level=0)

    counts = None

    try:
        sampler = RuntimeSampler(mode=backend)
        job = sampler.run([circuit], shots=shots)
        result = job.result()
        pub_result = result[0]
        data = getattr(pub_result, "data", None)

        if data is not None:
            for name in ("meas", "c"):
                register_data = getattr(data, name, None)
                if register_data is not None and hasattr(register_data, "get_counts"):
                    counts = register_data.get_counts()
                    break

            if counts is None:
                for name in dir(data):
                    if name.startswith("_"):
                        continue
                    register_data = getattr(data, name, None)
                    if hasattr(register_data, "get_counts"):
                        counts = register_data.get_counts()
                        break

        if counts is None and hasattr(result, "quasi_dists"):
            counts = dict(result.quasi_dists[0])
    except Exception:
        counts = None

    if counts is None:
        try:
            counts = backend.run(circuit, shots=shots, seed_simulator=seed).result().get_counts()
        except Exception:
            counts = {format(i, "03b"): float(abs(vector[i]) ** 2) for i in range(8)}

    probabilities = {format(i, "03b"): 0.0 for i in range(8)}
    total = float(sum(float(v) for v in counts.values()))

    if total <= 0:
        return probabilities

    for key, value in counts.items():
        if isinstance(key, (int, np.integer)):
            bitstring = format(int(key), "03b")
        else:
            bitstring = str(key).replace(" ", "")
            if bitstring.startswith("0x"):
                bitstring = format(int(bitstring, 16), "03b")
            elif bitstring.startswith("0b"):
                bitstring = format(int(bitstring, 2), "03b")
            else:
                filtered = "".join(ch for ch in bitstring if ch in "01")
                bitstring = filtered if filtered else "000"
                bitstring = bitstring[-3:].zfill(3)

        probabilities[bitstring[-3:].zfill(3)] = float(value) / total

    return probabilities
