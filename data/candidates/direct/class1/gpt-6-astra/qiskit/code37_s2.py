# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import BackendSamplerV2
from qiskit_aer import AerSimulator


def bv_algorithm(s):
    if not isinstance(s, str) or not s or any(bit not in "01" for bit in s):
        raise ValueError("s must be a nonempty string containing only 0s and 1s.")

    n = len(s)
    inputs = QuantumRegister(n, "input")
    ancilla = QuantumRegister(1, "ancilla")
    measurements = ClassicalRegister(n, "meas")
    circuit = QuantumCircuit(inputs, ancilla, measurements)

    circuit.x(ancilla[0])
    circuit.h(inputs)
    circuit.h(ancilla[0])

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.cx(inputs[index], ancilla[0])

    circuit.h(inputs)
    circuit.measure(inputs, measurements)

    sampler = BackendSamplerV2(backend=AerSimulator())
    result = sampler.run([circuit], shots=1024).result()
    bitstrings = result[0].data.meas.get_bitstrings()
    return [bitstrings, result]
