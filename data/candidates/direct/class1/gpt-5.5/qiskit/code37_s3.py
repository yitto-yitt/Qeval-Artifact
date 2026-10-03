# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.primitives import BackendSamplerV2
from qiskit_aer import AerSimulator


def bv_algorithm(s):
    s = str(s)
    if any(bit not in "01" for bit in s):
        raise ValueError("s must be a string of 0s and 1s")

    n = len(s)
    x = QuantumRegister(n, "x")
    y = QuantumRegister(1, "y")
    meas = ClassicalRegister(n, "meas")
    circuit = QuantumCircuit(x, y, meas)

    circuit.x(y[0])
    circuit.h(y[0])
    circuit.h(x)

    for i, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.cx(x[i], y[0])

    circuit.h(x)
    circuit.measure(x, meas)

    backend = AerSimulator()
    sampler = BackendSamplerV2(backend=backend)
    result = sampler.run([circuit], shots=1024).result()

    counts = result[0].data.meas.get_counts()
    bitstrings = list(counts.keys())

    return [bitstrings, result]
