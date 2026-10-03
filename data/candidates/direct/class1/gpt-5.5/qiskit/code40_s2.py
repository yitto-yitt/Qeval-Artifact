# EVAL_META: task_id=40, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

try:
    from qiskit_ibm_runtime import SamplerV2 as RuntimeSampler
except ImportError:
    from qiskit_ibm_runtime import Sampler as RuntimeSampler


def init_random_3qubit(desired_vector):
    vector = np.asarray(desired_vector, dtype=complex).flatten()
    if vector.size != 8:
        raise ValueError("desired_vector must contain exactly 8 amplitudes for a 3-qubit state.")

    norm = np.linalg.norm(vector)
    if norm == 0:
        raise ValueError("desired_vector must not be the zero vector.")
    vector = vector / norm

    qc = QuantumCircuit(3, 3)
    qc.initialize(vector, [0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])

    shots = 16384
    backend = AerSimulator(seed_simulator=12345)

    try:
        isa_qc = transpile(qc, backend, seed_transpiler=12345)
        try:
            sampler = RuntimeSampler(mode=backend)
        except TypeError:
            sampler = RuntimeSampler(backend)

        job = sampler.run([isa_qc], shots=shots)
        result = job.result()
        pub_result = result[0]
        data = pub_result.data

        bit_array = None
        for name in ("c", "meas"):
            try:
                bit_array = getattr(data, name)
                break
            except Exception:
                pass

        if bit_array is None:
            try:
                first_key = next(iter(data.keys()))
                bit_array = data[first_key]
            except Exception:
                bit_array = None

        if bit_array is not None and hasattr(bit_array, "get_counts"):
            counts = bit_array.get_counts()
        elif hasattr(result, "quasi_dists"):
            quasi = result.quasi_dists[0]
            counts = {}
            for key, value in quasi.items():
                bitstring = format(key, "03b") if isinstance(key, int) else str(key).replace(" ", "")
                counts[bitstring] = float(value) * shots
        else:
            counts = backend.run(qc, shots=shots).result().get_counts()
    except Exception:
        counts = backend.run(qc, shots=shots).result().get_counts()

    total = float(sum(counts.values())) if counts else 1.0
    distribution = {format(i, "03b"): 0.0 for i in range(8)}

    for key, value in counts.items():
        if isinstance(key, int):
            bitstring = format(key, "03b")
        else:
            bitstring = str(key).replace(" ", "")
            if bitstring.startswith("0x"):
                bitstring = format(int(bitstring, 16), "03b")
            else:
                bitstring = bitstring.zfill(3)[-3:]
        distribution[bitstring] = distribution.get(bitstring, 0.0) + float(value) / total

    return distribution
