# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import BackendSamplerV2
from qiskit_aer import AerSimulator


def bv_algorithm(s):
    s = str(s)
    if any(bit not in "01" for bit in s):
        raise ValueError("s must be a string of 0s and 1s")

    n = len(s)
    x = QuantumRegister(n, "x")
    y = QuantumRegister(1, "y")
    c = ClassicalRegister(n, "c")
    circuit = QuantumCircuit(x, y, c)

    circuit.x(y[0])
    circuit.h(y[0])
    circuit.h(x)

    for i, bit in enumerate(s):
        if bit == "1":
            circuit.cx(x[i], y[0])

    circuit.h(x)

    for i in range(n):
        circuit.measure(x[i], c[n - 1 - i])

    backend = AerSimulator(seed_simulator=12345)
    sampler = BackendSamplerV2(backend=backend)
    result = sampler.run([circuit], shots=1024).result()

    counts = result[0].data.c.get_counts()
    bitstrings = sorted(counts.keys(), key=lambda k: (-counts[k], k))

    return [bitstrings, result]
