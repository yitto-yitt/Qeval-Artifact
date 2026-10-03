# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator


def bv_algorithm(s):
    s = str(s)
    if any(bit not in "01" for bit in s):
        raise ValueError("s must be a string of 0s and 1s")

    n = len(s)
    shots = 1024

    x = QuantumRegister(n, "x")
    y = QuantumRegister(1, "y")
    c = ClassicalRegister(n, "c")
    circuit = QuantumCircuit(x, y, c)

    circuit.h(x)
    circuit.x(y[0])
    circuit.h(y[0])

    for i, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.cx(x[i], y[0])

    circuit.h(x)
    circuit.measure(x, c)

    backend = AerSimulator()

    def _bitstrings_from_counts(counts):
        return sorted(counts.keys(), key=lambda key: (-counts[key], key))

    def _counts_from_v2_result(res):
        pub_result = res[0]
        data = pub_result.data
        if hasattr(data, "c"):
            return data.c.get_counts()
        if hasattr(data, "keys"):
            key = list(data.keys())[0]
            return data[key].get_counts()
        return data.get_counts()

    try:
        from qiskit.primitives import BackendSamplerV2

        sampler = BackendSamplerV2(backend=backend)
        result = sampler.run([(circuit,)], shots=shots).result()
        counts = _counts_from_v2_result(result)
        bitstrings = _bitstrings_from_counts(counts)
        return [bitstrings, result]
    except Exception:
        pass

    try:
        from qiskit_aer.primitives import SamplerV2

        sampler = SamplerV2(default_shots=shots)
        result = sampler.run([circuit]).result()
        counts = _counts_from_v2_result(result)
        bitstrings = _bitstrings_from_counts(counts)
        return [bitstrings, result]
    except Exception:
        pass

    try:
        from qiskit_aer.primitives import Sampler

        sampler = Sampler(run_options={"shots": shots})
        result = sampler.run([circuit]).result()
        quasi = result.quasi_dists[0]
        try:
            probs = quasi.binary_probabilities(num_bits=n)
        except TypeError:
            probs = quasi.binary_probabilities(n)
        bitstrings = sorted(
            [key.replace(" ", "") for key, value in probs.items() if value > 1e-12],
            key=lambda key: (-probs.get(key, probs.get(key.replace(" ", ""), 0)), key),
        )
        return [bitstrings, result]
    except Exception:
        pass

    compiled = transpile(circuit, backend)
    result = backend.run(compiled, shots=shots).result()
    counts = result.get_counts(compiled)
    bitstrings = _bitstrings_from_counts(counts)
    return [bitstrings, result]
