# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

try:
    from qiskit.primitives import BackendSamplerV2
except Exception:
    BackendSamplerV2 = None

try:
    from qiskit_aer.primitives import Sampler as AerSampler
except Exception:
    AerSampler = None


def bv_algorithm(s):
    s = str(s)
    if any(bit not in "01" for bit in s):
        raise ValueError("s must be a string of 0s and 1s")

    n = len(s)
    shots = 1024

    circuit = QuantumCircuit(n + 1, n)
    ancilla = n

    circuit.x(ancilla)
    circuit.h(range(n + 1))

    for qubit, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.cx(qubit, ancilla)

    circuit.h(range(n))
    circuit.measure(range(n), range(n))

    backend = AerSimulator(seed_simulator=12345)

    if BackendSamplerV2 is not None:
        sampler = BackendSamplerV2(backend=backend)
        job = sampler.run([circuit], shots=shots)
        result = job.result()

        data = result[0].data
        if hasattr(data, "c"):
            counts = data.c.get_counts()
        else:
            key = list(data.keys())[0]
            counts = getattr(data, key).get_counts()

        bitstrings = sorted(counts.keys())
        return [bitstrings, result]

    sampler = AerSampler(run_options={"shots": shots, "seed": 12345})
    job = sampler.run(circuit)
    result = job.result()

    quasi = result.quasi_dists[0]
    probabilities = quasi.binary_probabilities(num_bits=n)
    bitstrings = sorted(bit for bit, probability in probabilities.items() if probability > 0)

    return [bitstrings, result]
