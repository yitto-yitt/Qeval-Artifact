# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit.primitives import BackendSamplerV2
from qiskit_aer import AerSimulator


def bv_algorithm(s):
    if not isinstance(s, str) or not s or any(bit not in "01" for bit in s):
        raise ValueError("s must be a nonempty string of 0s and 1s.")

    n = len(s)
    qubits = QuantumRegister(n + 1, "q")
    measurements = ClassicalRegister(n, "meas")
    circuit = QuantumCircuit(qubits, measurements)

    circuit.x(n)
    circuit.h(range(n + 1))

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.cx(index, n)

    circuit.h(range(n))
    circuit.measure(range(n), measurements)

    backend = AerSimulator()
    compiled_circuit = transpile(circuit, backend)
    sampler = BackendSamplerV2(backend=backend)
    result = sampler.run([compiled_circuit], shots=1024).result()
    bitstrings = result[0].data.meas.get_bitstrings()

    return [bitstrings, result]
