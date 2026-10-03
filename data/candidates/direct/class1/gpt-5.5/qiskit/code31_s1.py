# EVAL_META: task_id=31, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def sampler_qiskit():
    qr = QuantumRegister(2, "q")
    cr = ClassicalRegister(2, "c")
    circuit = QuantumCircuit(qr, cr)
    circuit.h(qr[0])
    circuit.cx(qr[0], qr[1])
    circuit.measure(qr, cr)

    backend = AerSimulator(seed_simulator=42)
    isa_circuit = transpile(circuit, backend=backend, seed_transpiler=42)

    shots = 1024
    sampler = Sampler(mode=backend)
    sampler.options.default_shots = shots

    result = sampler.run([isa_circuit]).result()
    pub_result = result[0]

    counts = pub_result.data.c.get_counts()
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
