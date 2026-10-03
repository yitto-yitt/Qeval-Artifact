# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.primitives import BackendSamplerV2
from qiskit_aer import AerSimulator


def bv_algorithm(s):
    if not isinstance(s, str) or not s or any(bit not in "01" for bit in s):
        raise ValueError("s must be a nonempty string of 0s and 1s.")

    n = len(s)
    circuit = QuantumCircuit(n + 1, n)

    circuit.x(n)
    circuit.h(range(n + 1))

    for qubit, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.cx(qubit, n)

    circuit.h(range(n))
    circuit.measure(range(n), range(n))

    sampler = BackendSamplerV2(backend=AerSimulator())
    result = sampler.run([circuit], shots=1024).result()
    bitstrings = result[0].data.c.get_bitstrings()

    return [bitstrings, result]
